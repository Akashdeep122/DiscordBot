import random
import json
def randomwanted(Names,message):

    
  random_function_selector =[
			    kill,kill,kill,kill,killyourself, revive,calm,calm,maketraps,maketraps,collectbullets]
  valuerecv = random.choice(random_function_selector)(Names,message)
  return valuerecv

def kill(Names,message):
  with open('Dead.json') as f:
    dead = json.load(f)
  Alive = list(Names)
  try:
    a = random.choice(Alive)
  except:
    revive(Names,message)
  b = random.choice(Alive)
 
  if a == b:
    try:
      return randomwanted(Names,message)
    except RecursionError:
      value = "A winner is to be announced soon"
      return value
  elif a != b:
    chances = random.randint(1,10)
    if chances <= 5:
      bullet = random.randint(1,70)
      if Names[a] >= bullet:
        Names[a] = Names[a] - bullet

        oppobullets = Names[b]
        del Names[b]
        Names[a] = oppobullets+Names[a]
        dead.append(b)
        print("all ok")
        replies = [f"**{a}** killed **{b}** with {bullet} bullets and Collected all **{b}**'s bullets , now they have **{Names[a]}** bullets",f"**{a} threw a sticky grenade in air which hit right on **{b}**'s head RIP , and They found his body and Collected His bullets",f"**{a}** yeeted a sticky grenade in air which hit right on **{b}**'s face, and He found his body and Collected His bullets",f"**{a}** were wasting bullets randomly on the mountain which hit **{b}** badly and they died RIP, They Collected all the bullets",f"YIKES. **{a}** showed no mercy and blasted **{b}** into outer-space with their gun.",f"**{a}** killed **{b}** with a stone , what a combat master",f"**{a}** were playing codm in real life and killed **{b}** with a knife LOL"]
        val = "<:PepeKill:868508463037317210>"+random.choice(replies)

        json.dump(dead, open('Dead.json', 'w'))
        json.dump(Names, open('Names.json', 'w'))
        #val = "<:PepeKill:868508463037317210>"+val
        return val
      else:
        oppobullets = random.randint(1,70)
        if Names[b] < oppobullets:
          return kill(Names,message)
        Names[a] = 0
        Names[b] = Names[b]-oppobullets
        #bulletswithme = Names[a]
        del Names[a]
        dead.append(a)
        with open('Dead.json', 'w') as f:
          json.dump(dead, f)
        with open('Names.json', 'w') as f:
          json.dump(Names, f)
        a = f"**{a}**"
        b = f"**{b}**"

        replies = [f"{a} tried to kill {b} with thier gun but they didnt have enough bullets and then {b} killed them back with {oppobullets} RIP and as {a} spent all thier bullets, {b} couldnt get a single bullet",f"{a} threw a sticky grenade in air which hit right on {b} but the bomb was fake and {b} killed them with a grenade which blasted all the bullet's gunpowder",f"{a} were shooting bullets randomly on the mountain and spent all thier bullets but {b} killed them with a 6x scope lmao but {a} already spent all his bullets",f"YIKES. {b} showed no mercy and blasted {a} into outer-space with their gun."]
        val = random.choice(replies)
        val = "<:PepeKill:868508463037317210>"+val
        return val
    elif chances > 5 and chances < 10 or chances == 10:
      bullet = random.randint(1,70)
      oppobullet = random.randint(1,70)
      print(Names[a])
      if Names[a] >= bullet and Names[b] >= oppobullet:
        Names[a] = Names[a] - bullet
        Names[b] = Names[b] - oppobullet

        oppobullets = Names[b]
        del Names[b]
        Names[a] = oppobullets+Names[a]
        dead.append(b)
        print("all ok")
        a = f"**{a}**"
        b = f"**{b}**"
        replies = [f"{a} killed {b} with {bullet} bullets and {b} also shot them {oppobullet}, but the end winner was {a} and they collected all thier bullets",f"{a} threw a sticky grenade in air which hit right on {b}'s body , and {b} was left with low hp and tried to kill them with some bullets but {a} was the winner and  Collected {b}'s bullets",f"{a} were shooting bullets randomly on the mountain which hit on {b}, but they also tried to kill but lost RIP, They Collected all the bullets",f"YIKES. {a} showed no mercy and had a huge fight with {b} but {a} blasted {b} into outer-space with their gun."]
        val = "<:PepeKill:868508463037317210>"+random.choice(replies)
        del a
        del b
        json.dump(dead, open('Dead.json', 'w'))
        json.dump(Names, open('Names.json', 'w'))
        #val = "<:PepeKill:868508463037317210>"+val
        return val
      else:
        Names[a] = 0
        Names[b] = 0
        replies = [f"{a} and {b} were both out of bullets and then they ran away LOL",f"{a} and {b} were so noob that they litteraly wasted all thier bullets",f"{a} and {b} both dont know to aim and they ended up wasting all bullets"]
        val = random.choice(replies)
        with open('Names.json', 'w') as f:
          json.dump(Names, f)
        with open('Dead.json', 'w') as f:
          json.dump(dead, f)
        val = "<:CatCry:826795857105256449>"+val
        return val
        
        
def killyourself(Names,message):
  Alive = Names.keys()
  with open('Dead.json') as f:
    dead = json.load(f)
  a = random.sample(Alive,1)
  print(a)
  a = str(a[0])
  del Names[a]
  dead.append(a)
  with open('Dead.json', 'w') as f:
          print(dead)
          json.dump(dead, f)
  with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)
  a = f"**{a}**"

  replies = [f"{a} Died Themselves Because they were sad from life",f"{a} climbed a Tall tree to hunt a Chicken but died Falling From it",f"{a} Were Throwing a Sticky Grenade but Forgot to wear nonStick Gloves , Which Exploded on Them RIP",f"A Lion was Running and saw {a} and killed them RIP",f"{a} Was trying to make a house with gravel which fell on him LOL",f"{a} tried to make a few traps for Someone , but ended up eating them himself LOL RIP"]
  val = random.choice(replies)
  del a
  val = "<:RIP:868510474008940594>"+val
  return val
  
def revive(Names,message):
  with open('Dead.json') as f:
    dead = json.load(f)
  if len(dead) == 0:
    a = randomwanted(Names,message)
    return a

  a = random.choice(dead)
  dead.remove(a)
  Names[a] = 40
  a = f"**{a}**"
  replies = [f"God gave {a} another chance to live",f"{a} were faking death as they were sleeping",f"{a}'s body joined back itself and they got revived",f"God thought that This guy {a} may get another chance, so here is he back",f"{a} were faking death to escape thier enemy but he just found 1 reload of thier gun (40 bullets)"]
  with open('Dead.json', 'w') as f:
          print(dead)
          json.dump(dead, f)
  with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)
  del a
  val = random.choice(replies)
  val = "<:heart:868509472933417030>"+val
  return val

def calm(Names,message):
  Alive = Names.keys()
  a = random.sample(Alive,1)
  print(a)
  a = str(a[0])
  a = f"**{a}**"
  replies = [f"{a} were resting peacefully in thier tent",f"{a} were taking a walk to admire the flowers",f"{a} bought a ps9 and began playing on it",f"{a} were so busy playing games on thier laptop",f"{a} were having a peaceful day but they didnt know that they were being followed"]
  del a
  val = random.choice(replies)
  val = "<:Popcorn:868511638435811331>"+val
  #val = "<:heart:868509472933417030>"
  return val

def maketraps(Names,message):
  Alive = Names.keys()
  try:
    a = random.sample(Alive,1)
  except ValueError:
    return randomwanted(Names,message)
  chances = random.randint(1,10)
  if chances <= 5:
    b = random.sample(Alive,1)
    del Names[str(b[0])]
    if a == b:
      return maketraps(Names,message)
    with open('Dead.json') as f:
      dead = json.load(f)
    dead.append(b)
    a = str(a[0])
    a = f"**{a}**"
    b = str(b[0])
    b = f"**{b}**"

    replies = [f"{a} Made some food traps in {b}'s food storage and {b} ended up eating them and died rip",f"{a} decided to put a dead spider in {b}'s lunchbox",f"{a} put a bomb in {b}'s ps9 and when they played it , it exploded so hard",f"{b} was killed by poison when they picked up the tiger claw by {a}"]
    val = random.choice(replies)
    return "<:poison:936140340228931584>"+val
  else:
    b = random.sample(Alive,1)
    if a == b:
      return maketraps(Names,message)
    a = str(a[0])
    a = f"**{a}**"
    b = str(b[0])
    b = f"**{b}**"

    replies = [f"{a} Made some food traps in {b}'s food storage and {b} Didnt eat them lol",f"{a} made poisonous traps for {b} but they survived ",f"{a} put a bomb in {b}'s ps9 And the bomb didnt work LOL",f"{b} was almost killed when they picked up the tiger claw by {a} but they used a adrealdine dose"]
    val = random.choice(replies)
    return "<:poison:936140340228931584>"+val

def collectbullets(Names,message):
  Alive = Names.keys()
  try:
    a = str(random.sample(Alive,1)[0])
  except ValueError:
    return randomwanted(Names,message)
  Names[a] = Names[a]+20
  a = f"**{a}**"

  replies = [f"{a} were playing on thier ps9 and when they finished , they found some bullets on the floor",f"{a} were looking on the flowers when a reload of thier bullets were scattered",f"{a} set a bomb nearby to catch someone but they ended up finding some bullets",f"{a} were running to get a place to kill and found 20 bullets on floor COOL"]
  val = random.choice(replies)
  return "<:bullets:936142362038640641>"+val


  
