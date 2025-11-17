# Assets   

| ID     | Name                    | Availability    | Integrity                                             | Confidentiality | Reasoning                                                                                | Description |
| ------ | ----------------------- | --------------- | ----------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------- | ----------- |
| A-DISP | Fish Food Dispenser     | DS-UNDERFEEDING | DS-UNDERFEEDING DS-OVERFEEDING                        |                 |                                                                                          |             |
| A-AO   | Analog Voltage          | DS-UNDERFEEDING | DS-UNDERFEEDING DS-OVERFEEDING                        |                 |                                                                                          |             |
| A-EL   | Embedded Linux          | DS-UNDERFEEDING | DS-UNDERFEEDING DS-OVERFEEDING DS-NETWORK             |                 |                                                                                          |             |
| A-FC   | Feeding Controller      | DS-UNDERFEEDING | DS-UNDERFEEDING DS-OVERFEEDING                        |                 |                                                                                          |             |
| A-WEB  | Web Server              | DS-CONFIG       | DS-UNDERFEEDING DS-OVERFEEDING DS-NETWORK DS-AUTHDATA |                 |                                                                                          |             |
| A-FS   | Feeding Schedule Files  | DS-UNDERFEEDING | DS-UNDERFEEDING DS-OVERFEEDING                        |                 |                                                                                          |             |
| A-AUTH | API Authentication Data | DS-CONFIG       | DS-UNDERFEEDING DS-OVERFEEDING                        | DS-AUTHDATA     |                                                                                          |             |
| A-CERT | Server Certificate      | DS-CONFIG       | DS-CONFIG                                             | DS-AUTHDATA     | A stolen certificate can be used to pose as the server and to steal authentication data. |             |
