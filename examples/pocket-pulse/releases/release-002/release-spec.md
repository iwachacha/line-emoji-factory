# Pocket Pulse release-002 Static Sticker Spec

## Basic Information
- Brand: Pocket Pulse
- Release: release-002
- Status: qa
- Item type: static-sticker
- Package type: sticker
- Set count: 8
- Count reason: LINE-supported minimum static sticker set for audit and first release testing.
- Concept: larger single-send status replies using the same Pocket Pulse signal mascot.
- Role in brand: prove the brand can expand from inline emoji to sticker-sized conversation blocks.

## Set Architecture
| Slot | Purpose | Single-send meaning | Sticker send line |
| --- | --- | --- | --- |
| 01 OK | acknowledge | I saw it and it is fine. | OK |
| 02 WAIT | pause | Please wait briefly. | WAIT |
| 03 DONE | completion | Finished. | DONE |
| 04 THX | thanks | Thanks. | THX |
| 05 FYI | notice | For your information. | FYI |
| 06 SOON | near future | I will handle it soon. | SOON |
| 07 SOS | help | I need help. | SOS |
| 08 LATER | defer | I will come back later. | LATER |

## Product Notes
- Static sticker content images stay within 370 x 320 and use even dimensions.
- Main image is 240 x 240 and shows the brand core without slot-specific text overload.
- Chat tab is 96 x 74 and remains readable as a small signal.

## Review Notes
- No advertising, release date, discount, free, or giveaway language.
- No external messenger or internet-service references.
- No corporate logo-like composition.
