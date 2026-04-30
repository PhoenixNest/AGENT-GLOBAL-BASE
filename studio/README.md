# Game Studios

Independent game studios operating under the organization. Each studio has its own workflow, team, and reference materials, but reports to the parent company's Chief Officers.

## Studios

| Studio                          | Focus             | Engine        | Status   |
| ------------------------------- | ----------------- | ------------- | -------- |
| [Casual Games](./casual-games/) | Casual mini-games | Unity 6.3 LTS | Planning |

## Adding a New Studio

To establish a new studio, create a folder at `studio/<studio-name>/` with the following structure:

```
studio/<studio-name>/
├── README.md                    # Studio overview and navigation
├── library/                     # Reference documentation
│   ├── overview/                # Studio charter, strategic brief
│   ├── topics/                  # Cross-cutting strategies
│   └── reference/               # External resources and link collections
├── pipeline/                    # Studio-specific development workflow
├── projects/                    # Individual game projects
└── team/                        # Personnel and crew profiles
    └── crew/                    # Agent profiles, skills, pipeline artifacts
```
