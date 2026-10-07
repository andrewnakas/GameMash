//! Realism look: physical sky and sun, HDR tonemapping, bloom, and, where
//! the GPU allows it (native / WebGPU builds), ambient occlusion and TAA.
//! The WebGL2 build gets a cheaper but matched look (filmic tonemap, fog,
//! hemisphere ambient).

use bevy::anti_alias::taa::TemporalAntiAliasing;
use bevy::camera::Exposure;
use bevy::core_pipeline::tonemapping::Tonemapping;
use bevy::light::{CascadeShadowConfigBuilder, light_consts::lux};
use bevy::light::{Atmosphere, AtmosphereEnvironmentMapLight, atmosphere::ScatteringMedium};
use bevy::pbr::{AtmosphereSettings, ScreenSpaceAmbientOcclusion};
use bevy::post_process::bloom::Bloom;
use bevy::prelude::*;

/// Debug switch (native): GAMEMASH_NOFX=ssao,taa,atmo,shadow,bloom
fn off(name: &str) -> bool {
    std::env::var("GAMEMASH_NOFX").map(|v| v.split(',').any(|x| x == name)).unwrap_or(false)
}

/// High quality = native or the WebGPU web build.
pub const HIGH_QUALITY: bool = cfg!(any(not(target_arch = "wasm32"), feature = "webgpu"));

#[derive(Component)]
pub struct Sun;

pub struct LookPlugin;

impl Plugin for LookPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_sun);
        if HIGH_QUALITY {
            app.insert_resource(GlobalAmbientLight::NONE);
        } else {
            app.insert_resource(GlobalAmbientLight { color: Color::srgb(0.72, 0.8, 0.95), brightness: 900.0, ..default() });
        }
    }
}

/// Late-afternoon sun: long shadows read as real light on concrete.
fn spawn_sun(mut commands: Commands, mut media: ResMut<Assets<ScatteringMedium>>) {
    let cascades = CascadeShadowConfigBuilder {
        num_cascades: if HIGH_QUALITY { 4 } else { 1 },
        first_cascade_far_bound: 12.0,
        maximum_distance: if HIGH_QUALITY { 220.0 } else { 60.0 },
        ..default()
    }
    .build();
    let sun_dir = Transform::from_xyz(-0.55, 0.42, -0.72).looking_at(Vec3::ZERO, Vec3::Y);
    commands.spawn((
        Sun,
        DirectionalLight {
            illuminance: if HIGH_QUALITY { lux::RAW_SUNLIGHT } else { 9_000.0 },
            color: Color::srgb(1.0, 0.96, 0.9),
            shadow_maps_enabled: HIGH_QUALITY && !off("shadow"),
            ..default()
        },
        cascades,
        sun_dir,
    ));
    if HIGH_QUALITY && !off("atmo") {
        commands.spawn(Atmosphere::earth(media.add(ScatteringMedium::earth(256, 256))));
    }
}

/// Look components for the main camera, attached at spawn (the atmosphere
/// pipeline must see them on the camera's first frame).
pub fn main_camera_look() -> impl Bundle {
    let base = (Tonemapping::AgX, Bloom { intensity: 0.08, ..Bloom::NATURAL });
    (
        base,
        if HIGH_QUALITY { Exposure { ev100: 13.5 } } else { Exposure { ev100: 9.7 } },
    )
}

/// Physical sky, IBL, TAA and SSAO on the high-quality path, attached in the
/// same command batch as the camera spawn.
pub fn attach_high_quality(cam: &mut EntityCommands) {
    if HIGH_QUALITY {
        if !off("atmo") {
            // Cheaper LUTs: the sky barely changes, so low sample counts and
            // small tables look the same at a fraction of the GPU cost.
            let light = std::env::var("GAMEMASH_ATMO_FULL").is_err();
            let settings = if light {
                AtmosphereSettings {
                    transmittance_lut_size: UVec2::new(128, 64),
                    transmittance_lut_samples: 16,
                    multiscattering_lut_dirs: 16,
                    multiscattering_lut_samples: 8,
                    sky_view_lut_size: UVec2::new(192, 96),
                    sky_view_lut_samples: 8,
                    aerial_view_lut_size: UVec3::new(16, 16, 16),
                    aerial_view_lut_samples: 4,
                    aerial_view_lut_max_distance: 2.0e3,
                    ..default()
                }
            } else {
                AtmosphereSettings::default()
            };
            cam.insert(settings).remove::<DistanceFog>();
            if !off("envmap") {
                let size = std::env::var("GAMEMASH_ENVSIZE").ok().and_then(|v| v.parse().ok()).unwrap_or(128u32);
                cam.insert(AtmosphereEnvironmentMapLight { size: UVec2::splat(size), ..default() });
            }
        }
        if !off("taa") {
            cam.insert((Msaa::Off, TemporalAntiAliasing::default()));
        }
        if !off("ssao") {
            cam.insert((Msaa::Off, ScreenSpaceAmbientOcclusion::default()));
        }
    }
    if off("bloom") {
        cam.remove::<Bloom>();
    }
}

/// The same look for secondary cameras (portal views), minus temporal effects.
pub fn secondary_camera_look() -> impl Bundle {
    (Tonemapping::AgX, if HIGH_QUALITY { Exposure { ev100: 13.5 } } else { Exposure { ev100: 9.7 } })
}
