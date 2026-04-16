# Studio Hardware — Workstation Specification

**Document Type:** Hardware Reference  
**Last Updated:** April 10, 2026  
**Owner:** CTO Office

---

## Standard Workstation

Every team member is equipped with the following device. No supplementary hardware is currently planned — the entire game development pipeline must be executed using these devices.

| Component   | Specification                                   |
| ----------- | ----------------------------------------------- |
| **Model**   | ASUS Zenbook Pro 14 Duo OLED (UX8402VV)         |
| **CPU**     | Intel Core i9-13900H (14-core, up to 5.4 GHz)   |
| **GPU**     | NVIDIA GeForce RTX 4060 8GB GDDR6               |
| **RAM**     | 32GB LPDDR5 (soldered, not upgradable)          |
| **Storage** | 1TB NVMe SSD                                    |
| **Display** | 14.5" 2.8K OLED 120Hz, touchscreen, 100% DCI-P3 |
| **OS**      | Windows 11 Home Chinese Edition (家庭中文版)    |

---

## Role Suitability Assessment

| Role                           | Meets Requirements? | Notes                                                                                     |
| ------------------------------ | ------------------- | ----------------------------------------------------------------------------------------- |
| Unity Engineering              | ✅ Yes              | RTX 4060 handles URP rendering; IL2CPP builds run fine on i9-13900H                       |
| Technical Artist (shader work) | ✅ Yes              | RTX 4060 8GB sufficient for shader compilation and GPU profiling                          |
| 3D Artist (Blender/Maya)       | ⚠️ Adequate         | Low-poly casual game assets fine; sustained rendering/baking will thermal-throttle        |
| 2D Artist (Photoshop/Krita)    | ✅ Yes              | OLED 100% DCI-P3 is excellent for 2D art                                                  |
| VFX Artist                     | ⚠️ Adequate         | Unity VFX Graph runs on RTX 4060; complex particles may stress thermals                   |
| Audio Designer                 | ✅ Yes              | Audio work is lightweight; 32GB RAM is overkill (good)                                    |
| Composer (chiptune)            | ✅ Yes              | Chiptune composition is extremely lightweight                                             |
| Game Designer / Producer       | ✅ Yes              | Figma, Unity Editor, documents — no heavy workloads                                       |
| QA Engineer                    | ✅ Yes              | Test execution on laptop is standard                                                      |
| DevOps / Build Engineer        | ⚠️ Adequate         | Cloud Build offloads heavy work; local builds will thermal-throttle on sustained compiles |

---

## Known Constraints

| Constraint                                        | Impact                                                                             | Mitigation                                                                                      |
| ------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Thermal throttling at 85W** (CPU+GPU sustained) | Long Unity builds, lightmap baking, and 3D rendering slow down after 10–15 minutes | Keep builds incremental; avoid full rebuilds; schedule heavy work for cloud CI                  |
| **1TB storage per machine**                       | Unity project + libraries + assets + build outputs can exceed 500GB per project    | Use cloud storage (Git LFS, cloud asset pipeline); aggressive cleanup of Library/Builds folders |
| **14.5" screen**                                  | Art review and level design on a small screen                                      | Use Unity multi-window layout efficiently; external monitor if docking stations available       |
| **Soldered 32GB RAM** (not upgradable)            | Fine for current scope; limits future scaling                                      | 32GB is sufficient for 2–3 year horizon                                                         |
| **No desktop workstations**                       | No dedicated high-power machine for heavy tasks                                    | Offload heavy work to cloud (Unity Cloud Build, CI/CD pipeline)                                 |
| **Battery ~5 hours**                              | Tethered to power during work hours                                                | Standard for creator laptop; not a dealbreaker in office                                        |

---

## Software Stack (Confirmed)

| Category             | Tool                                       | Rationale                                         |
| -------------------- | ------------------------------------------ | ------------------------------------------------- |
| **Game Engine**      | Unity 6.3 LTS                              | Primary development platform                      |
| **IDE**              | Visual Studio 2022 / Rider for Unity       | C# scripting                                      |
| **Version Control**  | Git + Git LFS                              | Code + binary asset management                    |
| **2D Art**           | Photoshop / Krita                          | Asset creation and editing                        |
| **3D Art**           | Blender                                    | Low-poly modeling for casual games                |
| **Audio DAW**        | Reaper                                     | SFX and music production                          |
| **Chiptune**         | Deflemask / FamiTrack / Magical 8-bit Plug | 8-bit audio synthesis                             |
| **Audio Middleware** | FMOD Studio (free tier)                    | Adaptive audio design + Unity integration         |
| **Design/Prototype** | Figma                                      | UI/UX design, concept prototyping                 |
| **CI/CD**            | GitHub Actions + Unity Cloud Build         | Automated builds and testing                      |
| **Backend**          | PlayFab (Indie tier, free)                 | Managed game backend with self-hosting capability |

---

## Document Version History

| Version | Date           | Author     | Changes                                 |
| ------- | -------------- | ---------- | --------------------------------------- |
| v1      | April 10, 2026 | CTO Office | Initial hardware specification document |

---

_End of Studio Hardware Specification_
