import requests
import os
import json
import csv

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
os.environ['BEARER_TOKEN']='AAAAAAAAAAAAAAAAAAAAAHi3YAEAAAAAUfqBztgNjVuJPKKPHjm8hYq4Vto%3DS7VuxnrLeT3MymrRAkNhTi1yAtvS6qnOPt1lnGGRoOmyQ5sg92'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/recent"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r

def connect_to_endpoint(params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception(response.status_code, response.text)
    return response.json()

#return the json response
def run_query(keyword, granularity):
    print(keyword)
    query_club = {'query': keyword,'granularity': granularity} #keyword is the name for search, granularity can be day, hour or minute for the separation
    json_response = connect_to_endpoint(query_club)
    #print(json_response["meta"]["total_tweet_count"])
    name = "results_clubs/data_" + keyword + ".json"
    with open(name, 'a') as outfile:
        json.dump(json_response, outfile)
    return json_response

def create_list_times(line):
    list_per_time = []
    for time in line["data"]:
        list_per_time.append([time["start"]])
    return list_per_time

def add_to_csv(header, list, granularity):   #header is the name of the clubs, list is the list of count per time slot
    list_times_existing = []
    exists = False
    #read
    if os.path.exists("result_per_"+ granularity + ".csv"):    #checks if the file already exists or not
        exists = True
        csv_file = open("result_per_"+ granularity + ".csv", "r", encoding='utf-8', newline='')
        csv_existing = csv.reader(csv_file)
        for row in csv_existing:
            list_times_existing.append(row[0])
        csv_file.close()
    #write
    csv_file = open("result_per_"+ granularity + ".csv", "a", encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    if not exists:
        writer.writerow(header)
    for time_element in list:
        print(time_element[0])
        if time_element[0] not in list_times_existing and time_element[0][14] == '0':
            writer.writerow(time_element)
    csv_file.close()

    return True

#finalement pas utilisé
def labels_fct(granularity):
    query_test = {'query': "test",'granularity': granularity} #keyword is the name for search, granularity can be day, hour or minute for the separation
    json_response = connect_to_endpoint(query_test)
    labels = []
    for time_slot in json_response["data"]:
        labels.append(time_slot["start"])
    return labels

#finalement pas utilisé
def header_clubs(input_file, granularity):
    list = ["time_slots"]
    for readline in input_file:
        list.append(readline.strip())
    csv_file = open("result_per_"+ granularity + ".csv", "a", encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list)


def count_ligue1(file, granularity): #granularity can be 'day', 'hour', 'minute'
    #labels =labels_fct() #recuperer le nom des lignes (time_slot)
    f = open( file + ".txt", 'r', encoding='utf-8')
    header_list = ["time_slots"]
    keyword = ""
    list_per_time = []
    zero_is_first = 0
    for club_line in f:  #for clubs
        if (club_line != "" or club_line != "\n"):
            header_list.append(club_line.strip())   #initialize the first line with the name of the clubs in the columns
            if zero_is_first == 0:
                keyword = '#' + club_line.strip() #club without "\n"
                result =run_query(keyword, granularity)
                list_per_time = create_list_times(result)   #list with the times
                index = 0
                for time in result["data"]:
                  list_per_time[index].append(time["tweet_count"])
                  index += 1
                zero_is_first += 1
            else:
                keyword = '#' + club_line.strip()
                result =run_query(keyword, granularity)
                index = 0
                for time in result["data"]:
                    list_per_time[index].append(time["tweet_count"])
                    index += 1
    add_to_csv(header_list, list_per_time, granularity)

    #print(header_list)
    #print(" ")
    #print(list_per_time)

    return True
    
            


def main():
    #header_clubs("list_clubs")
    count_ligue1("list_clubs_abrev", 'hour')   #second argument is 'day', 'hour' or'minute'
    #print(json.dumps(json_response, indent=4, sort_keys=True))



if __name__ == "__main__":
    main()