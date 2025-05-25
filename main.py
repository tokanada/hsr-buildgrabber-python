import enka
import asyncio
import json

cache = enka.cache.SQLiteCache()

sub_stat_dict = {
   1: [33.87,38.103755,42.33751], # HP
   2: [16.935,19.051877,21.168754], # ATK
   3: [16.935,19.051877,21.168754], # DEF
   4: [0.03456,0.03888,0.0432], # HP%
   5: [0.03456,0.03888,0.0432], # ATK%
   6: [0.0432,0.0486,0.054], # DEF%
   7: [2,2.3,2.6], # SPD
   8: [0.02592,0.02916,0.0324], # CR
   9: [0.05184,0.05832,0.0648], # CDMG
   10: [0.03456,0.03888,0.0432], # EHR
   11: [0.03456,0.03888,0.0432], # RES
   12: [0.05184,0.05832,0.0648] # BE
}

def find_closest_number_index(numbers, count, target):
    values = []
    for number in numbers:
       values.append(number * count)

    closest_index = 0
    min_difference = abs(values[0] - target)

    for i, value in enumerate(values):
       difference = abs(value - target)
       if difference < min_difference:
          min_difference = difference
          closest_index = i

    return closest_index

def get_character_name(res, i):
    return res.characters[i].name

def get_character_id(res, i):
    return res.characters[i].id

def get_character_level(res, i):
    return res.characters[i].level

def get_character_promotion(res, i):
    return res.characters[i].ascension

def get_character_rank(res, i):
    return res.characters[i].eidolons_unlocked

def get_lightcone_id(res, i):
    return res.characters[i].light_cone.id

def get_lightcone_rank(res, i):
    return res.characters[i].light_cone.superimpose

def get_lightcone_level(res, i):
    return res.characters[i].light_cone.level

def get_lightcone_promotion(res, i):
    return res.characters[i].light_cone.ascension

def get_relic_list(res, i):
    relic_list = []
    character_relic_list = res.characters[i].relics

    for idx, relic in enumerate(character_relic_list):
        subStatList = relic.sub_affix_list
        relic_entry = f"{relic.id},{relic.level},{relic.main_affix_id},{len(subStatList)}"

        for i in range(1, len(relic.stats)):
            sub_stat_roll_type = find_closest_number_index(sub_stat_dict[subStatList[i-1].id], subStatList[i-1].cnt,relic.stats[i].value)
            substat_string = f",{subStatList[i-1].id}:{subStatList[i-1].cnt}:{sub_stat_roll_type}"
            relic_entry += substat_string

        relic_list.append(relic_entry)

    return relic_list

async def main() -> None:
    async with enka.HSRClient(cache=cache) as client:

        while True:
            try: 
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                print("=======================")
                print("=  HSR Relic Fetcher  =")
                print("=======================")

                uid = int(input("\nEnter UID: "))
                print(uid)
                character_index = int(input("Enter Character Postion (on Showcase): ")) - 1

                print("\nRetrieving Information...")
                response = await client.fetch_showcase(uid)
                print("\nResponse received\n")

                print(response.player.nickname,"\n\n")

                character_dict = {
                    "name": get_character_name(response, character_index),
                    "id": get_character_id(response, character_index),
                    "hp": 100,
                    "sp": 50,
                    "level": get_character_level(response, character_index),
                    "promotion": get_character_promotion(response, character_index),
                    "rank": get_character_rank(response, character_index),
                    "lightcone": {
                        "id": get_lightcone_id(response, character_index),
                        "rank": get_lightcone_rank(response, character_index),
                        "level": get_lightcone_level(response, character_index),
                        "promotion": get_lightcone_promotion(response, character_index)
                    },
                    "relics": get_relic_list(response, character_index),
                    "use_technique": True
                }

                try:
                    json_output_string = json.dumps(character_dict, indent=4)

                    print(json_output_string)
                except TypeError as e:
                    print(f"Error: Could not serialize the dictionary to JSON. Reason: {e}")
                    print("Please ensure all items in your dictionary are JSON serializable.")
                    print("(e.g., basic types like str, int, float, bool, list, dict, None)")
                    print("(Custom objects, sets, or date/time objects need special handling.)")

                rp = input("\nTry another? (Y/n) ")
                
                if rp == "n" or rp == "N":
                    break

            except KeyboardInterrupt:
                print("\nInput interrupted by user (Ctrl+C). Exiting gracefully.")
                break  # Exit the loop
            except EOFError:
                print("\nEnd of input detected (Ctrl+D on Unix-like systems). Exiting gracefully.")
                break  # Exit the loop
            except Exception as e:
                # Catch any other unexpected errors during input or processing
                print(f"\nAn unexpected error occurred: {e}. Exiting gracefully.")
                break # Exit the loop

asyncio.run(main())
