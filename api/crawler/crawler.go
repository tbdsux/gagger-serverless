package crawler

import (
	"crypto/rand"
	"math/big"
	rander "math/rand"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/anaskhan96/soup"
)

// randomly picks a number from the given slice and maximum
func randomPicker(slice []string) int {
	s := rander.NewSource(time.Now().Unix())
	r := rander.New(s)
	random := r.Intn(len(slice))
	return random
}

// Getter => gets a meme from a random chosen source
func Getter() map[string]string {
	meme := make(map[string]string)

	// select a random meme website
	sites := []string{"memedroid", "gifvif"}
	randomIndex := randomPicker(sites)

	ransite := sites[randomIndex]
	if ransite == "gifvif" {
		meme["website"] = "gif-vif.com"
		meme["meme"] = GifVif()
	} else if ransite == "memedroid" {
		meme["website"] = "memedroid.com"
		meme["meme"] = MemeDroid()
	}

	// return the meme map
	return meme
}

// Compiler => compiles the return element of the two websites
func Compiler(website string) map[string]string {
	meme := make(map[string]string)

	if website == "gifvif" {
		meme["website"] = "gif-vif.com"
		meme["meme"] = GifVif()
	} else if website == "memedroid" {
		meme["website"] = "memedroid.com"
		meme["meme"] = MemeDroid()
	} else {
		meme["website"] = website
		meme["meme"] = "website not yet supported"
	}

	return meme
}

// GifVif => returns a slice of gifs from gif-vif.com
func GifVif() string {
	website := "https://www.gif-vif.com/category/funny/"

	// randomly get memes from a random page number
	randomNum := func() string {
		nbig, err := rand.Int(rand.Reader, big.NewInt(374))
		if err != nil {
			panic(err)
		}

		num := nbig.Int64()

		if num == 0 {
			num = 1
		}
		return strconv.FormatInt(num, 10)
	}

	// chooose a random gif from the links
	resp, err := soup.Get(website + randomNum())
	if err != nil {
		os.Exit(1)
	}
	doc := soup.HTMLParse(resp)
	containers := doc.FindAll("div", "id", "gif_container")
	var links []string
	for _, link := range containers {
		raw := link.Find("a")
		links = append(links, raw.Attrs()["href"])
	}

	index := randomPicker(links)

	// get the meme from the chosen link
	resp, err = soup.Get(links[index])
	if err != nil {
		os.Exit(1)
	}

	doc = soup.HTMLParse(resp)
	src := doc.Find("div", "id", "gif_div")
	gif := src.Find("source").Attrs()["src"]

	return gif
}

// MemeDroid => returns a slice of memes from memedroid.com
func MemeDroid() string {
	website := "https://www.memedroid.com/memes/random"

	resp, err := soup.Get(website)

	if err != nil {
		os.Exit(1)
	}

	doc := soup.HTMLParse(resp)

	containers := doc.FindAll("div", "class", "item-aux-container")

	var memes []string

	for _, meme := range containers {
		raw, err := meme.Find("img").Attrs()["src"]
		if err {
			if strings.HasPrefix(raw, "https://images") {
				memes = append(memes, raw)
			}
		}

	}

	index := randomPicker(memes)

	return memes[index]
}
