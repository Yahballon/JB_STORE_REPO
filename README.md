<p align="center">

# JAILBREAK STORE REPO

**Community repository for open-source PlayStation 5 homebrew applications.**

</p>

JB_STORE_REPO is a community-maintained repository for **PS5 homebrew applications, tools, emulators, utilities and other legal open-source software**.

The goal of this repository is to provide clean metadata and download information that can be used by compatible PS5 homebrew stores and installers.

This project is intended exclusively for legitimate homebrew development and distribution.

## Purpose

JB_STORE_REPO provides repository data for PS5 homebrew software.

Applications included here should generally be:

- Open source.
- Freely distributable.
- Created specifically for PS5 homebrew or compatible with PS5 homebrew.
- Distributed by the original developer or with permission.
- Hosted on a legitimate public source such as GitHub.
- Free from copyrighted commercial game content.
- Free from proprietary Sony system files.
- Free from console keys, credentials or other protected secrets.

The repository itself does not operate a commercial software store.

It is an index for community-developed homebrew software.

## Supported content

Examples of software that may be accepted:

- Open-source PS5 homebrew applications.
- Homebrew games.
- Emulators distributed under an appropriate open-source license.
- File managers.
- Media applications.
- Development tools.
- Debugging utilities.
- Network utilities.
- Homebrew launchers.
- Open-source ports.
- Community tools.
- Experimental PS5 projects.
- Legal front-ends and clients.
- Applications created specifically for the PS5 homebrew ecosystem.

Projects must have appropriate redistribution rights.

## No warez

**Warez is strictly prohibited.**

JB_STORE_REPO does **not** accept, distribute, index or intentionally link to pirated commercial software.

The following content is not permitted:

- Pirated PS5 games.
- Pirated PS4 games.
- Commercial game packages.
- Cracked commercial applications.
- Paid software distributed without permission.
- Repacked commercial games.
- Warez releases.
- Copyrighted game files.
- Copyrighted DLC.
- Unauthorized game updates.
- Commercial ROM collections.
- Commercial ISO collections.
- Proprietary BIOS files when redistribution is not authorized.
- Sony system software or firmware files distributed without authorization.
- Console encryption keys.
- Decryption keys.
- Authentication credentials.
- Stolen certificates.
- DRM secrets.
- Content intended primarily to facilitate copyright infringement.
- Links to piracy or warez hosting services.

Do **not** submit this material through commits, pull requests, issues, repository metadata or external download links.

## No copyrighted games

Emulators and open-source emulator front-ends may be accepted.

Copyrighted commercial games are **not** included.

For example, an emulator may be distributed when its own license allows redistribution, but commercial ROMs, ISOs, game images or other copyrighted game data must not be bundled with it.

Users are responsible for obtaining and using game content legally.

JB_STORE_REPO does not provide games.

## BIOS and firmware

Some homebrew applications or emulators may require external BIOS, firmware or system files.

Those files must **not** be included in this repository unless redistribution is explicitly authorized by the relevant copyright holder and applicable license.

Applications should require users to provide their own legally obtained files when necessary.

## Repository entries

Applications may be represented using metadata similar to:

```json
{
  "name": "Example Homebrew",
  "type": "app",
  "cover_image": "https://example.com/icon.png",
  "description": "Example open-source PS5 homebrew application.",
  "size_bytes": 12345678,
  "download_url": "https://github.com/example/project/releases/download/1.0/app.zip",
  "title_id": "PPSA00000",
  "version": "1.0.0",
  "format": "zip",
  "status": "available",
  "supported_by_store": true,
  "source_page": "https://github.com/example/project",
  "sha256": "example",
  "author": "Example Developer"
}
```

Metadata should be accurate and should point to legitimate project sources whenever possible.

## Submission rules

Before submitting an application, make sure that:

- The project is legitimate homebrew.
- The software can legally be redistributed.
- The download URL comes from a trusted source.
- The source repository is provided when available.
- The project license allows the intended distribution.
- No copyrighted commercial software is included.
- No ROMs, ISOs or commercial games are included.
- No proprietary Sony files are included.
- No console keys or credentials are included.
- The SHA-256 hash is correct when provided.
- The file size is correct.
- The Title ID is correct.
- The version number is correct.
- The description accurately represents the application.

Whenever possible, downloads should point directly to the developer's official GitHub release or another official distribution source.

## Pull requests

Pull requests are welcome for legitimate PS5 homebrew.

A pull request may be rejected if it contains or links to:

- Warez.
- Pirated games.
- Commercial applications.
- Unauthorized copyrighted files.
- Proprietary firmware.
- Console keys.
- Credentials.
- Malware.
- Misleading download links.
- Suspicious binaries.
- Projects without sufficient redistribution rights.
- Content that violates GitHub's policies.

Maintainers may request additional information about a project before accepting it.

Submission does not guarantee inclusion.

## Direct pushes

Do not use direct pushes to add unauthorized,
