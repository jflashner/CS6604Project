# PanelBench README

## Data

Motions and speeches are in the `data` folder. For each debate set, extract the
`.tar.gz` archive into the `preset` folder of Debatrix. The `gold` folder
contains true results of the debates; Debatrix doesn't need them, but you can
use them to verify Debatrix's judgments.

## Debatrix Config

Dimension and judge configs are in the `config` folder. For each debate set,
move the folder to the one extracted to `preset` in the previous section, and
rename it to `config`. Copy the other configs (`model.yml`, `manager.yml`,
`recorder.yml`) from `preset/example/config` in Debatrix to the renamed `config`
folder.
