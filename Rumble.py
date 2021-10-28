import random
import json
def randomchooser(Names,message,random_function_selector):
  valuerecv = random.choice(random_function_selector)(Names,message)
  return valuerecv

def kill(Names,message):
  with open('Dead.json') as f:
    dead = json.load(f)
  Alive = list(Names.keys())
  print(Alive)
  a = random.choice(Alive)
  b = random.choice(Alive)
 
  if a == b:
    try:
      kill(Names,message)
    except RecursionError:
      value = "A winner is to be announced soon"
      return value
  elif a != b:
    chances = random.randint(1,10)
    if chances > 5:
      bullet = random.randint(1,50)
      if Names[a] >= bullet:
        Names[a] = Names[a] - bullet
        oppobullets = Names[b]
        del Names[b]
        Names[a] = oppobullets+Names[a]
        dead.append(b)
        with open('Dead.json', 'w') as f:
          print(dead)
          json.dump(dead, f)
        with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)
        replies = [f"{a} killed {b} with {bullet} bullets and Collected all {b}'s bullets , now they have {Names[a]} bullets",f"{a} threw a sticky grenade in air which hit right on {b}'s head RIP , and They found his body and Collected His bullets",f"{a} yeeted a sticky grenade in air which hit right on {b}'s face, and He found his body and Collected His bullets",f"{a} were shooting bullets randomly on the mountain which hit all as headshots on {b} RIP, They Collected all the bullets",f"YIKES. {a} showed no mercy and blasted {b} into outer-space with their gun."]
        val = random.choice(replies)
        val = "<:PepeKill:868508463037317210>"+val
        return val
      else:
        oppobullets = random.randint(1,50)
        Names[a] = 0
        Names[b] = Names[b]-oppobullets
        #bulletswithme = Names[a]
        del Names[a]
        dead.append(a)
        with open('Dead.json', 'w') as f:
          print(dead)
          json.dump(dead, f)
        with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)

        replies = [f"{a} tried to kill {b} with thier gun but they didnt have enough bullets and then {b} killed them back with {oppobullets} RIP and as {a} spent all thier bullets, {b} couldnt get a single bullet",f"{a} threw a sticky grenade in air which hit right on {b} but the bomb was fake and {b} killed them with a grenade which blasted all the bullet's gunpowder",f"{a} were shooting bullets randomly on the mountain and spent all thier bullets but {b} killed them with a 6x scope lmao but {a} already spent all his bullets",f"YIKES. {b} showed no mercy and blasted {a} into outer-space with their gun."]
        val = random.choice(replies)
        val = "<:PepeKill:868508463037317210>"+val
        return val
    else:
      bullet = random.randint(1,50)
      oppobullet = random.randint(1,50)
      if Names[a] >= bullet and Names[b] >= oppobullet:
        Names[a] = Names[a] - bullet
        Names[b] = Names[b] - bullet

        oppobullets = Names[b]
        del Names[b]
        Names[a] = oppobullets+Names[a]
        dead.append(b)
        with open('Dead.json', 'w') as f:
          print(dead)
          json.dump(dead, f)
        with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)

        replies = [f"{a} killed {b} with {bullet} bullets and {b} also shot them {oppobullet}, but the end winner was {a} and they collected all thier bullets",f"{a} threw a sticky grenade in air which hit right on {b}'s body , and {b} was left with low hp and tried to kill them with some bullets but {a} was the winner and  Collected {b}'s bullets",f"{a} were shooting bullets randomly on the mountain which hit on {b}, but they also tried to kill but lost RIP, They Collected all the bullets",f"YIKES. {a} showed no mercy and had a huge fight with {b} but {a} blasted {b} into outer-space with their gun."]
        val = random.choice(replies)
        del a
        del b
        val = "<:PepeKill:868508463037317210>"+val
        return val
      else:
        c = random.choice(Alive)
        cbullet = random.randint(1,50)
        Names[c] = Names[c]-cbullet
        del Names[a]
        del Names[b]
        dead.append(b)
        dead.append(a)


        replies = [f"{a} and {b} were so close to each other but didnt even see them {c} saw them and killed them with his gun RIP, but forgot to take his bullets LMAO"]
        del c
        val = random.choice(replies)
        with open('Names.json', 'w') as f:
          print(Names)
          json.dump(Names, f)
        with open('Dead.json', 'w') as f:
          print(Names)
          json.dump(dead, f)
        val = "<:PepeKill:868508463037317210>"+val
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

  replies = [f"{a} Died Themselves Because they were sad from life",f"{a} climbed a Tall tree to hunt a Chicken but died Falling From it",f"{a} Were Throwing a Sticky Grenade but Forgot to wear nonStick Gloves , Which Exploded on Them RIP",f"A Lion was Running and saw {a} and killed them RIP"]
  val = random.choice(replies)
  del a
  val = "<:RIP:868510474008940594>"+val
  return val
  
def revive(Names,message):
  with open('Dead.json') as f:
    dead = json.load(f)
  if len(dead) == 0:
    a = "God didnt have anyone to revive so round off"
    return a

  a = random.choice(dead)
  dead.remove(a)
  Names[a] = 40
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
  replies = [f"{a} were resting peacefully in thier tent",f"{a} were taking a walk to admire the flowers",f"{a} bought a ps9 and began playing on it",f"{a} were so busy playing games on thier laptop",f"{a} were having a peaceful day but they didnt know that they were being followed"]
  del a
  val = random.choice(replies)
  val = "<:Popcorn:868511638435811331>"+val
  #val = "<:heart:868509472933417030>"
  return val