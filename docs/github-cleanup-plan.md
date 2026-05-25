# GitHub Repository Cleanup Plan

Updated: 2026-05-25 after Corbyn's rename/delete pass.

Corbyn has already completed the main rename/delete pass. This file now acts as a status note and follow-up checklist rather than a proposed rename plan.

## Current naming pattern

Corbyn used readable prefixes with title-style project names:

- `client_...` — paid/client work
- `personal_...` — personal/product work
- `Zz_...` — old/archived/legacy work pushed to the bottom of repo lists

## Active repos wired into the operating system

- `Falkurne/client_All_Project-Reports`
  - Purpose: static reporting hub and automated draft client updates.
  - Local clone: `/home/falkae/Projects/client_All_Project-Reports`
  - Local remote: updated.
- `Falkurne/client_Motofi_Broker-Marketplace`
  - Purpose: Motofi broker marketplace MVP.
  - Local clone: `/home/falkae/Projects/client_Motofi_Broker-Marketplace`
  - Local remote: updated.
  - Reporting source map: updated.
- `Falkurne/client_Eloanz_Website`
  - Purpose: ELoanz website and enquiry funnel.
  - Local clone: `/home/falkae/Projects/client_Eloanz_Website`
  - Local remote: updated.
  - Reporting source map: updated.

## Other retained repos

- `Falkurne/client_O2D_Chat-Simulator`
- `Falkurne/personal_GW2_Legendary-Tracker`
- `Falkurne/personal_Command-Center`
- `Falkurne/personal_Corbyn.net_Website`
- `Falkurne/Zz_Client_TGS_Website`
- `Falkurne/Zz_Archived_personal-openclaw` — already archived on GitHub.
- `Falkurne/Zz_Client_EFF_Mobile-App`

## No longer visible after cleanup

The older empty/duplicate/archive candidates from the initial plan are no longer returned by GitHub, so they appear to have been deleted or otherwise removed.

## Follow-up actions

1. Keep reporting automation pointed at:
   - `Falkurne/client_Eloanz_Website`
   - `Falkurne/client_Motofi_Broker-Marketplace`
2. Consider archiving these retained legacy repos if they should be read-only:
   - `Falkurne/Zz_Client_TGS_Website`
   - `Falkurne/Zz_Client_EFF_Mobile-App`
3. Local folder names now match the active GitHub repo names, and the draft report cron job workdir has been updated.
