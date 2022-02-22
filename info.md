[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

<p><a href="https://www.buymeacoffee.com/6rF5cQl" rel="nofollow" target="_blank"><img src="https://camo.githubusercontent.com/c070316e7fb193354999ef4c93df4bd8e21522fa/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76312e7376673f6c6162656c3d4275792532306d6525323061253230636f66666565266d6573736167653d25463025394625413525413826636f6c6f723d626c61636b266c6f676f3d6275792532306d6525323061253230636f66666565266c6f676f436f6c6f723d7768697465266c6162656c436f6c6f723d366634653337" alt="Buy me a coffee" data-canonical-src="https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&amp;message=%F0%9F%A5%A8&amp;color=black&amp;logo=buy%20me%20a%20coffee&amp;logoColor=white&amp;labelColor=b0c4de" style="max-width:100%;"></a></p>

# Home Assistant custom integration for fire protection in Hungary

This custom component provides fire protection information from nebih.gov.hu based on county (valid only for Hungary).

The state of the sensor will be the fire ban level of the county set (0: no restriction; 1: fire ban).

#### Installation
The easiest way to install it is through [HACS (Home Assistant Community Store)](https://github.com/hacs/integration),
search for <i>Fire Protection Hungary</i> in the Integrations.<br />

#### Configuration:
Define sensor with the following configuration parameters:<br />

---
| Name | Optional | `Default` | Description |
| :---- | :---- | :------- | :----------- |
| name | **Y** | `fire_protection_hu` | name of the sensor |
| county_id | **Y** | `20` | county identifier |
---

county_id is the serial value of the county when counties are sorted alphabetically (1: Baranya, 2: Bács-Kiskun;...; 19: Zala; 20: Budapest).

![Meteo alerts attributes](https://raw.githubusercontent.com/amaximus/fire_protection_hu/main/fire_protection_hu.png)

#### Example
```
platform: fire_protection_hu
county_id: 12 # Pest county
```

#### Lovelace UI
If you want to show an alert use the following:

```
type: conditional
conditions:
  - entity: sensor.fire_protection_hu
    state_not: '0'
card:
  type: custom:button-card
  size: 30px
  styles:
    label:
      - font-size: 90%
    card:
      - height: 80px
    icon:
      - color: >
          [[[
            var f_level = states['sensor.fire_protection_hu'].state;
            if ( f_level == 0 ) {
              return "var(--paper-item-icon-color)";
            } else if ( f_level == 1 ) {
              return "var(--paper-item-icon-active-color)";
            }
            return "black";
          ]]]
  label: "Tűzgyújtási tilalom"
  show_label: true
  show_name: false
  entity: sensor.fire_protection_hu
  color_type: icon
```

## Thanks

Thanks to all the people who have contributed!

[![contributors](https://contributors-img.web.app/image?repo=amaximus/fire_protection_hu)](https://github.com/amaximus/fire_protection_hu/graphs/contributors)
