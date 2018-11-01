package main

import (
	"errors"
	"flag"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/smtp"
	"strings"

	yaml "gopkg.in/yaml.v2"

	"github.com/golang/glog"
)

type People struct {
	Name     string
	Email    string
	Address  string
	Wishlist string
}

type Email struct {
	SmtpServer      string `yaml:"smtp_server"`
	Domain          string
	AccountAddress  string `yaml:"account_address"`
	AccountPassword string `yaml:"account_password"`
	Port            int
}

var test = flag.Bool("test", true, "Pass false to this flag to run for realsies")

var emailTemp = `Subject: Feelings: 2016 Secret Santa

 Hello %s,
 
 Thank you for participating in ths year's Feelings Secret Santa! Here is your assignment information:

 Name: %s

 Address: %s

 Hobbies/interests: %s
 
 Things to consider:
 - Please schedule your gift shipping so that it arrives as close to Christmas as possible, unless otherwise noted. Keep in mind that shipping times will generally be longer than normal during the holidays.
 - There is no strict limit to pricing, but $20-$30 is a good range to be in.
 - If you are having trouble deciding on a gift, feel free to ask around. Just be subtle, please.
 - If you are STILL having trouble deciding on a gift, here is a Dan-approved list of gifts that everyone will love: https://amzn.com/B014P8L66E, https://amzn.com/B01DVJMI0Q, https://amzn.com/B002ECDZCW, https://amzn.com/B01H0AX66W 
 - Feel free to message me (Daniel) if you have any questions or concerns.
 
 Sincerely,
 Daniel`

func main() {
	flag.Parse()
	peopleConfig, err := ioutil.ReadFile("people.yml")
	if err != nil {
		glog.Fatalf(`error reading "people.yml" file: %s`, err)
	}
	people := map[string]*People{}
	err = yaml.Unmarshal(peopleConfig, people)
	if err != nil {
		glog.Fatalf(`error unmarshaling people config: %s`, err)
	}

	var assignments map[string]string
	for {
		assignments, err = assign(people)
		if err == nil {
			break
		}
	}
	glog.Infof("assignments are %+v", assignments)

	emailConfig, err := ioutil.ReadFile("smtp.yml")
	if err != nil {
		glog.Fatalf(`error reading "smtp.yml" file: %s`, err)
	}
	email := &Email{}
	err = yaml.Unmarshal(emailConfig, email)
	if err != nil {
		glog.Fatalf(`error unmarshaling email config: %s`, err)
	}

	auth := smtp.PlainAuth("", email.AccountAddress, email.AccountPassword, email.SmtpServer)

	for santa, giftee := range assignments {
		config := people[giftee]
		emailMsg := fmt.Sprintf(emailTemp, strings.Title(santa), strings.Title(config.Name), config.Address, config.Wishlist)
		glog.V(3).Infof("emailMsg for %s  with email %s is %s", santa, people[santa].Email, emailMsg)
		if !*test {
			err := smtp.SendMail(fmt.Sprintf("%s:%d", email.SmtpServer, email.Port),
				auth, email.AccountAddress, []string{people[santa].Email}, []byte(emailMsg))
			if err != nil {
				glog.Fatalf("Failed to send email: %s", err)
			}
		}
	}
}

func assign(people map[string]*People) (map[string]string, error) {
	assignments := make(map[string]string, len(people))

	// Get the names of all the people participating (keys to people)
	names := []string{}
	for name := range people {
		names = append(names, name)
	}
	firstName := names[0]

	// For each santa, assign a random person, repicking the random person until it is
	// not the same as the santa
	for santa := range people {
		var giftee string
		var i int
		for {
			i = rand.Intn(len(names))
			giftee = names[i]
			if santa == giftee {
				if len(names) == 1 {
					// We are in the case where there is only once choice of giftee left, and it
					// is the santa. Exit and try again.
					return nil, errors.New("Bad")
				}
			} else {
				break
			}
		}
		assignments[santa] = giftee
		names = append(names[:i], names[i+1:]...)
	}

	// Check for short loops
	loopChecker := make(map[string]bool)
	for !loopChecker[firstName] {
		loopChecker[firstName] = true
		firstName = assignments[firstName]
	}
	if len(loopChecker) != len(assignments) {
		// There is a loop somewhere, otherwise we should've covered
		// everyone in assignments
		return nil, errors.New("Bad")
	}

	return assignments, nil
}
