import yaml
import random

from django.core.mail import send_mail
from django.conf import settings

def assign(people):
    """
    In: Dictionary with people an associated info
    Out: Different dictionary but that follows secret santa assignments, for one large loop
    """
    assignments = {}

    # Get names of all people participating (keys of people to name list)
    names = list(people.keys())
    firstName = names[0]


    # For each santa, assign a random person, repicking the random person until it is
    # not the same as the santa
    for santa in people:
        while True:
            giftee = random.choice(names)
            if santa == giftee:
                if len(names) == 1:
                    # We are in the case where there is only one giftee left and it's
                    # the same as santa. Exit and try again.
                    return None, True
            else:
                break


        assignments[santa] = giftee
        names.remove(giftee)

    # Check for short loops
    loopChecker = {}
    while firstName not in loopChecker:
        loopChecker[firstName] = True
        firstName = assignments[firstName]

    print(str(len(loopChecker)), str(len(assignments)))
    if len(loopChecker) != len(assignments):
        # There exists a loop otherwise everyone in assignments should be covered.
        return None, True


    return assignments, None


def email(santa_name, giftee_name, santa_email, giftee_address, giftee_hobbies):
    '''
    Sends an email based on santa and giftee information and assignment using django's
    email wrappers
    '''
    subject = "Feelings Secret Santa 2018"
    message = "Hello {},\n\nThank you for participating in this year's Feelings Secret Santa! Here is your assignment information:\n\n\tName: {}\n\tAddress: {}\n\tHobbies/Interests: {}\n\nThings to consider:\n- Please schedule your gift shipping so that it arrives as close to Christmas as possible, unless otherwise noted. Keep in mind that shipping times will generally be longer than normal during the holidays.\n- There is no strict limit to pricing, but $20-$30 is a good range to be in.\n- If you are having trouble deciding on a gift, feel free to ask around. Just be subtle, please.\n- Feel free to message me on Discord (dzy#0001) if you have any questions or concerns.\n\n\nSincerely,\nDnan".format(santa_name, giftee_name, giftee_address, giftee_hobbies)

    email_from = settings.EMAIL_HOST_USER
    recipient = [santa_email]

    send_mail(
        subject,
        message,
        email_from,
        recipient,
        fail_silently=False,
    )

    return True



# Read in YAML file without errors
# refer to people.yml for example

# change this to the real file before sending
with open("./secretsanta/scripts/people2.yml", "r") as stream:
    try:
        people = yaml.load(stream)
    except yaml.Error as exc:
        print(exc)

# make assignments for people (keys of a dict?)
while True:
    assignments, err = assign(people)
    if err is None:
        break

print(people)
print(assignments)

# send emails based on assignments
for santa, giftee in assignments.items():
    santa_name = people[santa]['name']
    giftee_name = people[giftee]['name']
    santa_email = people[santa]['email']
    giftee_address = people[giftee]['address']
    giftee_hobbies = people[giftee]['wishlist']

    email(santa_name, giftee_name, santa_email, giftee_address, giftee_hobbies)
