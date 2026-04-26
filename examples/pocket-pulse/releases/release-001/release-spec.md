# Pocket Pulse release-001 Static Emoji Spec

## Basic Information
- Brand: Pocket Pulse
- Release: release-001
- Status: qa
- Item type: static-emoji
- Package type: emoji
- Set count: 8
- Count reason: audit-sized minimum set for LINE-supported static emoji packaging.
- Concept: tiny status signals for inline daily coordination.
- Role in brand: prove the brand works at the smallest product surface.

## Set Architecture
| Slot | Purpose | Single-send meaning | Inline role |
| --- | --- | --- | --- |
| 001 OK | acknowledge | I saw it and it is fine. | confirmation suffix |
| 002 WAIT | pause | Hold briefly. | delay marker |
| 003 DONE | completion | This is finished. | closure marker |
| 004 THX | thanks | Thanks without extra warmth. | gratitude suffix |
| 005 FYI | notice | Light information notice. | attention marker |
| 006 SOON | near future | I will handle it shortly. | timing marker |
| 007 SOS | help | I need help or attention. | alert marker |
| 008 LATER | defer | I will come back later. | defer marker |

## Product Notes
- Every emoji uses the same round signal mascot.
- Labels are short ASCII to avoid metadata or font ambiguity during audit.
- Each slot varies by color and status mark so the set is not a recolor-only pack.

## Review Notes
- No external service names, logos, campaign text, sale language, or personal targeting.
- SOON is used as a timing state, not a release announcement.
- SOS is casual support language, not violence or emergency imagery.
