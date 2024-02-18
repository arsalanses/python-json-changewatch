package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
)

type Data struct {
	Items []struct {
		AvailableSeatCount uint8  `json:"availableSeatCount"`
		DepartureTime      string `json:"departureTime"`
	} `json:"items"`
}

func sendPostRequest(url string, payload map[string]interface{}) error {
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("error marshalling JSON payload: %w", err)
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonPayload))
	if err != nil {
		return fmt.Errorf("error creating POST request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("error sending POST request: %w", err)
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("error reading POST response body: %w", err)
	}

	fmt.Println("POST response:", string(respBody))
	return nil
}

func main() {
	url := os.Getenv("URL_ADDRESS")

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Error fetching JSON data:", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}

	var data Data
	err = json.Unmarshal(body, &data)
	if err != nil {
		fmt.Println("Error unmarshalling JSON data:", err)
		return
	}

	fmt.Println(data.Items)

	for _, item := range data.Items {
		parts := strings.Split(item.DepartureTime, ":")
		if len(parts) != 2 {
			fmt.Println("Invalid departure time format:", item.DepartureTime)
			return
		}

		departureHour, err := strconv.Atoi(parts[0])
		if err != nil {
			fmt.Println("Error converting departure hour to integer:", err)
			return
		}

		if (departureHour > 19) && (item.AvailableSeatCount > 0) {
			postURL := os.Getenv("TELEGRAM_BASE")

			text := fmt.Sprintf("AvailableSeatCount:%d,\n DepartureTime:%s", item.AvailableSeatCount, item.DepartureTime)

			payload := map[string]interface{}{
				"chat_id": os.Getenv("CHAT_ID"),
				"text":    text,
			}

			err := sendPostRequest(postURL, payload)
			if err != nil {
				fmt.Println("Error sending POST request:", err)
				return
			}
		}
	}
}
