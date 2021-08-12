import json
import logging
import requests
import app.io
import threading

'''
Main country class to find respective populations and name.
'''

class Country:
    LOGGER = logging.getLogger(__name__)
    GEONAMES_URL = "http://api.geonames.org/countryInfoJSON"
    GEONAMES_BACKUP_PATH = "geonames_population_mappings.json"

    # Fetching of the populations.
    def fetch_populations(save=False):
        """
        Returns a dictionary containing the population of each country fetched from the GeoNames.
        https://www.geonames.org/
        TODO: only skip writing to the filesystem when deployed with gunicorn, or handle concurent access, or use DB.
        :returns: The mapping of populations.
        :rtype: dict
        """
        LOGGER.info("Fetching populations...")

        # Mapping of populations
        mappings = {}

        # Fetch the countries.
        try:
            countries = requests.get(GEONAMES_URL, params={"username": "dperic"}, timeout=1.25).json()[
                "geonames"
            ]
            # Go through all the countries and perform the mapping.
            for country in countries:
                mappings.update({country["countryCode"]: int(country["population"]) or None})

            if mappings and save:
                LOGGER.info(f"Saving population data to {app.io.save(GEONAMES_BACKUP_PATH, mappings)}")
        except (json.JSONDecodeError, KeyError, requests.exceptions.Timeout) as err:
            LOGGER.warning(f"Error pulling population data. {err.__class__.__name__}: {err}")
            mappings = app.io.load(GEONAMES_BACKUP_PATH)
            LOGGER.info(f"Using backup data from {GEONAMES_BACKUP_PATH}")
        # Finally, return the mappings.
        LOGGER.info("Fetched populations")
        return mappings


    # Mapping of alpha-2 codes country codes to population.
    POPULATIONS = fetch_populations()

    # Retrieving.
    def country_population(country_code, default=None):
        """
        Fetches the population of the country with the provided country code.
        :returns: The population.
        :rtype: int
        """
        return POPULATIONS.get(country_code, default)

    LOGGER = logging.getLogger(__name__)

    # Default country code.
    DEFAULT_COUNTRY_CODE = "XX"

    # Mapping of country names to alpha-2 codes according to
    # https://en.wikipedia.org/wiki/ISO_3166-1.
    # As a reference see also https://github.com/TakahikoKawasaki/nv-i18n (in Java)
    # fmt: off
    COUNTRY_NAME__COUNTRY_CODE = {
        "Afghanistan"                                  : "AF",
        "Åland Islands"                                : "AX",
        "Albania"                                      : "AL",
        "Algeria"                                      : "DZ",
        "American Samoa"                               : "AS",
        "Andorra"                                      : "AD",
        "Angola"                                       : "AO",
        "Anguilla"                                     : "AI",
        "Antarctica"                                   : "AQ",
        "Antigua and Barbuda"                          : "AG",
        "Argentina"                                    : "AR",
        "Armenia"                                      : "AM",
        "Aruba"                                        : "AW",
        "Australia"                                    : "AU",
        "Austria"                                      : "AT",
        "Azerbaijan"                                   : "AZ",
        " Azerbaijan"                                  : "AZ",
        "Bahamas"                                      : "BS",
        "The Bahamas"                                  : "BS",
        "Bahamas, The"                                 : "BS",
        "Bahrain"                                      : "BH",
        "Bangladesh"                                   : "BD",
        "Barbados"                                     : "BB",
        "Belarus"                                      : "BY",
        "Belgium"                                      : "BE",
        "Belize"                                       : "BZ",
        "Benin"                                        : "BJ",
        "Bermuda"                                      : "BM",
        "Bhutan"                                       : "BT",
        "Bolivia, Plurinational State of"              : "BO",
        "Bolivia"                                      : "BO",
        "Bonaire, Sint Eustatius and Saba"             : "BQ",
        "Caribbean Netherlands"                        : "BQ",
        "Bosnia and Herzegovina"                       : "BA",
        # "Bosnia–Herzegovina"                         : "BA",
        "Bosnia"                                       : "BA",
        "Botswana"                                     : "BW",
        "Bouvet Island"                                : "BV",
        "Brazil"                                       : "BR",
        "British Indian Ocean Territory"               : "IO",
        "Brunei Darussalam"                            : "BN",
        "Brunei"                                       : "BN",
        "Bulgaria"                                     : "BG",
        "Burkina Faso"                                 : "BF",
        "Burundi"                                      : "BI",
        "Cambodia"                                     : "KH",
        "Cameroon"                                     : "CM",
        "Canada"                                       : "CA",
        "Cape Verde"                                   : "CV",
        "Cabo Verde"                                   : "CV",
        "Cayman Islands"                               : "KY",
        "Central African Republic"                     : "CF",
        "Chad"                                         : "TD",
        "Chile"                                        : "CL",
        "China"                                        : "CN",
        "Mainland China"                               : "CN",
        "Christmas Island"                             : "CX",
        "Cocos (Keeling) Islands"                      : "CC",
        "Colombia"                                     : "CO",
        "Comoros"                                      : "KM",
        "Congo"                                        : "CG",
        "Congo (Brazzaville)"                          : "CG",
        "Republic of the Congo"                        : "CG",
        "Congo, the Democratic Republic of the"        : "CD",
        "Congo (Kinshasa)"                             : "CD",
        "DR Congo"                                     : "CD",
        "Cook Islands"                                 : "CK",
        "Costa Rica"                                   : "CR",
        "Côte d'Ivoire"                                : "CI",
        "Cote d'Ivoire"                                : "CI",
        "Ivory Coast"                                  : "CI",
        "Croatia"                                      : "HR",
        "Cuba"                                         : "CU",
        "Curaçao"                                      : "CW",
        "Curacao"                                      : "CW",
        "Cyprus"                                       : "CY",
        "Czech Republic"                               : "CZ",
        "Czechia"                                      : "CZ",
        "Denmark"                                      : "DK",
        "Djibouti"                                     : "DJ",
        "Dominica"                                     : "DM",
        "Dominican Republic"                           : "DO",
        "Dominican Rep"                                : "DO",
        "Ecuador"                                      : "EC",
        "Egypt"                                        : "EG",
        "El Salvador"                                  : "SV",
        "Equatorial Guinea"                            : "GQ",
        "Eritrea"                                      : "ER",
        "Estonia"                                      : "EE",
        "Ethiopia"                                     : "ET",
        "Falkland Islands (Malvinas)"                  : "FK",
        "Falkland Islands"                             : "FK",
        "Faroe Islands"                                : "FO",
        "Faeroe Islands"                               : "FO",
        "Fiji"                                         : "FJ",
        "Finland"                                      : "FI",
        "France"                                       : "FR",
        "French Guiana"                                : "GF",
        "French Polynesia"                             : "PF",
        "French Southern Territories"                  : "TF",
        "Gabon"                                        : "GA",
        "Gambia"                                       : "GM",
        "The Gambia"                                   : "GM",
        "Gambia, The"                                  : "GM",
        "Georgia"                                      : "GE",
        "Germany"                                      : "DE",
        "Deutschland"                                  : "DE",
        "Ghana"                                        : "GH",
        "Gibraltar"                                    : "GI",
        "Greece"                                       : "GR",
        "Greenland"                                    : "GL",
        "Grenada"                                      : "GD",
        "Guadeloupe"                                   : "GP",
        "Guam"                                         : "GU",
        "Guatemala"                                    : "GT",
        "Guernsey"                                     : "GG",
        "Guinea"                                       : "GN",
        "Guinea-Bissau"                                : "GW",
        "Guyana"                                       : "GY",
        "Haiti"                                        : "HT",
        "Heard Island and McDonald Islands"            : "HM",
        "Holy See (Vatican City State)"                : "VA",
        "Holy See"                                     : "VA",
        "Vatican City"                                 : "VA",
        "Honduras"                                     : "HN",
        "Hong Kong"                                    : "HK",
        "Hong Kong SAR"                                : "HK",
        "Hungary"                                      : "HU",
        "Iceland"                                      : "IS",
        "India"                                        : "IN",
        "Indonesia"                                    : "ID",
        "Iran, Islamic Republic of"                    : "IR",
        "Iran"                                         : "IR",
        "Iran (Islamic Republic of)"                   : "IR",
        "Iraq"                                         : "IQ",
        "Ireland"                                      : "IE",
        "Republic of Ireland"                          : "IE",
        "Isle of Man"                                  : "IM",
        "Israel"                                       : "IL",
        "Italy"                                        : "IT",
        "Jamaica"                                      : "JM",
        "Japan"                                        : "JP",
        "Jersey"                                       : "JE",
        # Guernsey and Jersey form Channel Islands. Conjoin Guernsey on Jersey.
        # Jersey has higher population.
        # https://en.wikipedia.org/wiki/Channel_Islands
        "Guernsey and Jersey"                          : "JE",
        "Channel Islands"                              : "JE",
        # "Channel Islands"                              : "GB",
        "Jordan"                                       : "JO",
        "Kazakhstan"                                   : "KZ",
        "Kenya"                                        : "KE",
        "Kiribati"                                     : "KI",
        "Korea, Democratic People's Republic of"       : "KP",
        "North Korea"                                  : "KP",
        "Korea, Republic of"                           : "KR",
        "Korea, South"                                 : "KR",
        "South Korea"                                  : "KR",
        "Republic of Korea"                            : "KR",
        "Kosovo, Republic of"                          : "XK",
        "Kosovo"                                       : "XK",
        "Kuwait"                                       : "KW",
        "Kyrgyzstan"                                   : "KG",
        "Lao People's Democratic Republic"             : "LA",
        "Laos"                                         : "LA",
        "Latvia"                                       : "LV",
        "Lebanon"                                      : "LB",
        "Lesotho"                                      : "LS",
        "Liberia"                                      : "LR",
        "Libya"                                        : "LY",
        "Liechtenstein"                                : "LI",
        "Lithuania"                                    : "LT",
        "Luxembourg"                                   : "LU",
        "Macao"                                        : "MO",
        # TODO Macau is probably a typo. Report it to CSSEGISandData/COVID-19
        "Macau"                                        : "MO",
        "Macao SAR"                                    : "MO",
        "North Macedonia"                              : "MK",
        "Macedonia"                                    : "MK",
        "Madagascar"                                   : "MG",
        "Malawi"                                       : "MW",
        "Malaysia"                                     : "MY",
        "Maldives"                                     : "MV",
        "Mali"                                         : "ML",
        "Malta"                                        : "MT",
        "Marshall Islands"                             : "MH",
        "Martinique"                                   : "MQ",
        "Mauritania"                                   : "MR",
        "Mauritius"                                    : "MU",
        "Mayotte"                                      : "YT",
        "Mexico"                                       : "MX",
        "Micronesia, Federated States of"              : "FM",
        "F.S. Micronesia"                              : "FM",
        "Micronesia"                                   : "FM",
        "Moldova, Republic of"                         : "MD",
        "Republic of Moldova"                          : "MD",
        "Moldova"                                      : "MD",
        "Monaco"                                       : "MC",
        "Mongolia"                                     : "MN",
        "Montenegro"                                   : "ME",
        "Montserrat"                                   : "MS",
        "Morocco"                                      : "MA",
        "Mozambique"                                   : "MZ",
        "Myanmar"                                      : "MM",
        "Burma"                                        : "MM",
        "Namibia"                                      : "NA",
        "Nauru"                                        : "NR",
        "Nepal"                                        : "NP",
        "Netherlands"                                  : "NL",
        "New Caledonia"                                : "NC",
        "New Zealand"                                  : "NZ",
        "Nicaragua"                                    : "NI",
        "Niger"                                        : "NE",
        "Nigeria"                                      : "NG",
        "Niue"                                         : "NU",
        "Norfolk Island"                               : "NF",
        "Northern Mariana Islands"                     : "MP",
        "Norway"                                       : "NO",
        "Oman"                                         : "OM",
        "Pakistan"                                     : "PK",
        "Palau"                                        : "PW",
        "Palestine, State of"                          : "PS",
        "Palestine"                                    : "PS",
        "occupied Palestinian territory"               : "PS",
        "State of Palestine"                           : "PS",
        "The West Bank and Gaza"                       : "PS",
        "West Bank and Gaza"                           : "PS",
        "Panama"                                       : "PA",
        "Papua New Guinea"                             : "PG",
        "Paraguay"                                     : "PY",
        "Peru"                                         : "PE",
        "Philippines"                                  : "PH",
        "Pitcairn"                                     : "PN",
        "Poland"                                       : "PL",
        "Portugal"                                     : "PT",
        "Puerto Rico"                                  : "PR",
        "Qatar"                                        : "QA",
        "Réunion"                                      : "RE",
        "Reunion"                                      : "RE",
        "Romania"                                      : "RO",
        "Russian Federation"                           : "RU",
        "Russia"                                       : "RU",
        "Rwanda"                                       : "RW",
        "Saint Barthélemy"                             : "BL",
        "Saint Barthelemy"                             : "BL",
        "Saint Helena, Ascension and Tristan da Cunha" : "SH",
        "Saint Helena"                                 : "SH",
        "Saint Kitts and Nevis"                        : "KN",
        "Saint Kitts & Nevis"                          : "KN",
        "Saint Lucia"                                  : "LC",
        "Saint Martin (French part)"                   : "MF",
        "Saint Martin"                                 : "MF",
        "St. Martin"                                   : "MF",
        "Saint Pierre and Miquelon"                    : "PM",
        "Saint Pierre & Miquelon"                      : "PM",
        "Saint Vincent and the Grenadines"             : "VC",
        "St. Vincent & Grenadines"                     : "VC",
        "Samoa"                                        : "WS",
        "San Marino"                                   : "SM",
        "Sao Tome and Principe"                        : "ST",
        "São Tomé and Príncipe"                        : "ST",
        "Sao Tome & Principe"                          : "ST",
        "Saudi Arabia"                                 : "SA",
        "Senegal"                                      : "SN",
        "Serbia"                                       : "RS",
        "Seychelles"                                   : "SC",
        "Sierra Leone"                                 : "SL",
        "Singapore"                                    : "SG",
        "Sint Maarten (Dutch part)"                    : "SX",
        "Sint Maarten"                                 : "SX",
        "Slovakia"                                     : "SK",
        "Slovenia"                                     : "SI",
        "Solomon Islands"                              : "SB",
        "Somalia"                                      : "SO",
        "South Africa"                                 : "ZA",
        "South Georgia and the South Sandwich Islands" : "GS",
        "South Sudan"                                  : "SS",
        "Spain"                                        : "ES",
        "Sri Lanka"                                    : "LK",
        "Sudan"                                        : "SD",
        "Suriname"                                     : "SR",
        "Svalbard and Jan Mayen"                       : "SJ",
        "Eswatini"                                     : "SZ",  # previous name "Swaziland"
        "Swaziland"                                    : "SZ",
        "Sweden"                                       : "SE",
        "Switzerland"                                  : "CH",
        "Syrian Arab Republic"                         : "SY",
        "Syria"                                        : "SY",
        "Taiwan, Province of China"                    : "TW",
        "Taiwan*"                                      : "TW",
        "Taipei and environs"                          : "TW",
        "Taiwan"                                       : "TW",
        "Tajikistan"                                   : "TJ",
        "Tanzania, United Republic of"                 : "TZ",
        "Tanzania"                                     : "TZ",
        "Thailand"                                     : "TH",
        "Timor-Leste"                                  : "TL",
        "East Timor"                                   : "TL",
        "Togo"                                         : "TG",
        "Tokelau"                                      : "TK",
        "Tonga"                                        : "TO",
        "Trinidad and Tobago"                          : "TT",
        "Tunisia"                                      : "TN",
        "Turkey"                                       : "TR",
        "Turkmenistan"                                 : "TM",
        "Turks and Caicos Islands"                     : "TC",
        "Turks and Caicos"                             : "TC",
        "Tuvalu"                                       : "TV",
        "Uganda"                                       : "UG",
        "Ukraine"                                      : "UA",
        "United Arab Emirates"                         : "AE",
        "Emirates"                                     : "AE",
        "United Kingdom"                               : "GB",
        "UK"                                           : "GB",
        # Conjoin North Ireland on United Kingdom
        "North Ireland"                                : "GB",
        "United States"                                : "US",
        "US"                                           : "US",
        "United States Minor Outlying Islands"         : "UM",
        "Uruguay"                                      : "UY",
        "Uzbekistan"                                   : "UZ",
        "Vanuatu"                                      : "VU",
        "Venezuela, Bolivarian Republic of"            : "VE",
        "Venezuela"                                    : "VE",
        "Viet Nam"                                     : "VN",
        "Vietnam"                                      : "VN",
        "Virgin Islands, British"                      : "VG",
        "British Virgin Islands"                       : "VG",
        "Virgin Islands, U.S."                         : "VI",
        "U.S. Virgin Islands"                          : "VI",
        "Wallis and Futuna"                            : "WF",
        "Wallis & Futuna"                              : "WF",
        "Western Sahara"                               : "EH",
        "Yemen"                                        : "YE",
        "Zambia"                                       : "ZM",
        "Zimbabwe"                                     : "ZW",

        # see also
        # https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_(data_file)#Data_file
        # https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent
        "United Nations Neutral Zone"                  : "XD",
        "Iraq-Saudi Arabia Neutral Zone"               : "XE",
        "Spratly Islands"                              : "XS",

        # "Diamond Princess"                             : default_country_code,
        # TODO "Disputed Territory" conflicts with `default_country_code`
        # "Disputed Territory"                         : "XX",

        # "Others" has no mapping, i.e. the default val is used

        # ships:
        # "Cruise Ship"
        # "MS Zaandam"
    }

    # fmt: on
    def country_code(value):
        """
        Return two letter country code (Alpha-2) according to https://en.wikipedia.org/wiki/ISO_3166-1
        Defaults to "XX".
        """
        code = COUNTRY_NAME__COUNTRY_CODE.get(value, DEFAULT_COUNTRY_CODE)
        if code == DEFAULT_COUNTRY_CODE:
            # log at sub DEBUG level
            LOGGER.log(5, f"No country code found for '{value}'. Using '{code}'!")

        return code


    __shared_instance = None
    @staticmethod
    def getInstance():
        """Static Access Methods """
        if Country.__shared_instance == None:
            Country()
        return Country.__shared_instance

    def __init__(self) -> None:
        """ Virtual Private Constructor"""
        if Country.__shared_instance != None:
            raise Exception("This is a singleton class !")
        else:
            Country.__shared_instance = self

if __name__ == '__country__':
    # create object of the singleton class
    obj = Country()
    print(obj)

    # pick the instance of the class
    obj = Country.getInstance()
    print(obj)
