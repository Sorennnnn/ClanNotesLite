import pickle

# Main
def main():
    cmd = input('\n'+cmdheader)
    sqb = 0
    newcmd = ''
    for char in cmd:
        if (debug <= 1):
            print(char)
        if (char == '['):
            sqb = 1
        elif (char == ']'):
            sqb = 0
        if (char == ' ' and not sqb):
            char = dummystring
        if (char not in '[]'):
            newcmd+=char

    newcmd = newcmd.split(dummystring)
    if (debug <= 2):
        print(newcmd)

    if (newcmd[0] in list(cmddict.keys())):
        if (debug > 0):
            try:
                cmddict[newcmd[0]][0](*newcmd[1:])
            except:
                print('-Command failed-')
                print('Type \'help\' to list commands.')
        else:
            cmddict[newcmd[0]][0](*newcmd[1:])
    else:
        print('-Command \'{}\' not recognised-'.format(newcmd[0]))
        print('Type \'help\' to list commands.')

# Background Functions
def getplayer(player):
    notelist = notesdict.get(player, -1)
    if (notelist == -1):
        notelist = []
    return notelist

def savelist(player, notelist):
    notesdict[player] = notelist
    save()

def addnote(notelist, noteID, *args):
    note = [noteID]
    
    if (noteID == 0):
        pass
    elif (noteID == 1):
        note.append(args[0])
        note.append(args[1])
    elif (noteID == 2):
        note.append(args[0])

    notelist.append(note)
    return notelist

def getnoatkcount(notelist):
    count = 0
    for note in notelist:
        if (note[0] == 0):
            count+=1
    return count

def save():
    with open('ClanNotesData.pickle', 'a') as file:
        pass
    with open('ClanNotesData.pickle', 'wb') as file:
        pickle.dump(notesdict, file)

# Foreground Functions
def helpcmd(*args):
    if (len(args) > 0):
        key = cmddict.get(args[0], -1)
        if (key == -1):
            print('Command \'{}\' not recognised.'.format(args[0]))
        else:
            key = args[0]
            print('  \'{}{}\'\n  {}\n'.format(key, cmddict[key][1], cmddict[key][2]))
    else:
        print('NOTE: Enclose text in square brackets if you want the command line to ignore spaces within.')
        print('NOTE: Arguments preceeded by \'~\' are optional.')
        print('Commands:')
        print()
        for key in sorted(list(cmddict.keys())):
            print('  \'{}{}\'\n  {}\n'.format(key, cmddict[key][1], cmddict[key][2]))

def noatk(player, *args):
    notelist = getplayer(player)
    proceed = 1
    if (len(notelist) > 0):
        if (notelist[0][0] == 2):
            proceed = 0
            print('KICKED: {}'.format(notelist[0][1]))
    if (proceed):
        addnote(notelist, 0)
        savelist(player, notelist)
        print('Added {}\'s noatk'.format(player))

def kick(player, reason, *args):
    deleteplayer(player)
    notelist = getplayer(player)
    addnote(notelist, 2, reason)
    savelist(player, notelist)
    print('Kicked {}.'.format(player))

def pardon(player, reason, *args):
    deleteplayer(player)
    writenote(player, 'pardon', reason)
    print('Pardoned {}.'.format(player))

def view(player, *args):
    notelist = getplayer(player)
    if (len(notelist)>0):
        print('Showing notes for \'{}\':'.format(player))
        if (notelist[0][0] == 2):
            print('KICKED: {}'.format(notelist[0][1]))
        else:
            print('  No Attack Streak: {}'.format(getnoatkcount(notelist)))
            for note in notelist:
                if (note[0] == 1):
                    print('  \'{}\': {}'.format(note[1], note[2]))
                
    else:
        print('Player \'{}\' not found (or player has no notes).'.format(player))
    print()

def viewallnotes(*args):
    for key in sorted(list(notesdict.keys())):
        count = 0
        notelist = getplayer(key)
        for note in notelist:
            if (note[0] == 1):
                view(key)
                break

def viewallkicks(*args):
    for key in sorted(list(notesdict.keys())):
        count = 0
        notelist = getplayer(key)
        for note in notelist:
            if (note[0] == 2):
                view(key)
                break

def getnoatks(*args):
    if (len(args) > 0):
        low = int(args[0])
    else:
        low = 1
    print('Showing players who have not attacked recently: ')
    for key in sorted(list(notesdict.keys())):
        noatkcount = getnoatkcount(getplayer(key))
        if (noatkcount >= low):
            print('  {} ({})'.format(key, str(noatkcount)))

def deleteplayer(player, *args):
    pop = notesdict.pop(player, None)
    if (pop is None):
        print('\'{}\' not found.'.format(player))
    else:
        save()
        print('Successfully deleted \'{}\'.'.format(player))
        
def listplayers(*args):
    print('Showing names of all players: ')
    for key in sorted(list(notesdict.keys())):
        print('  {}'.format(key))

def renameplayer(player, name, *args):
    pop = notesdict.pop(player, None)
    if (pop is None):
        print('\'{}\' not found.'.format(player))
    else:
        savelist(name, pop)
        print('Successfully renamed \'{}\' to \'{}\'.'.format(player, name))

def writenote(player, name, text, *args):
    notelist = getplayer(player)
    proceed = 1
    if (len(notelist) > 0):
        if (notelist[0][0] == 2):
            proceed = 0
            print('KICKED: {}'.format(notelist[0][1]))
    if (proceed):
        savelist(player, addnote(notelist, 1, name, text))
        view(player)

def deletenote(player, name, *args):
    success = 0
    notelist = getplayer(player)
    for count, note in enumerate(notelist):
        if note[0] > 0:
            if note[1] == name:
                notelist.pop(count)
                savelist(player, notelist)
                success = 1
                break
    else:
        print('Note \'{}\' not found.'.format(name))
        view(player)
        
    if (success):
        print('Success')

def addatk(player, *args):
    notelist = getplayer(player)
    notelist = [value for ind, value in enumerate(notelist) if notelist[ind][0]!=0]
    savelist(player, notelist)
    print('Success')

def doquit(*args):
    quit()

# Program
if __name__=='__main__':
    dummystring = '**&^*%'
    cmdheader = '>> '
    debug = 3 # 0 = Full, unprotected debug. 1 = Full, protected debug. 2 = Partial Debug. 3 = No debug.
    cmddict = {
            'quit':[doquit, '', 'Exits ClanNotesLite.'],
            'help':[helpcmd, '', 'Shows command help.'],
            'noatk':[noatk, ' <player>', 'Adds a noatk note to <player>.'],
            'atk':[addatk, ' <player>', 'Removes all noatks from <player>.'],
            'view':[view, ' <player>', 'Views the notes for <player>.'],
            'viewnotes':[viewallnotes, '', 'View the notes for all players with notes.'],
            'viewkicks':[viewallkicks, '', 'View the notes for all players who have been kicked'],
            'viewnoatks':[getnoatks, ' ~<min>', 'Lists players with noatk notes.'],
            'kick':[kick, ' <player> <reason>', 'Virtually kicks <player> for <reason>'],
            'pardon':[pardon, ' <player> <reason>', 'Virtually pardons <player>, leaving note with <reason>.'],
            'delete':[deleteplayer, ' <player>', 'Deletes all notes for <player>.'],
            'viewplayers':[listplayers, '', 'Lists all players.'],
            'rename':[renameplayer, ' <player> <name>', 'Renames <player> to <name>.'],
            'addnote':[writenote, ' <player> <name> <text>', 'Adds a note, <name> reading <text> to <player>.'],
            'deletenote':[deletenote, ' <player> <name>', 'Deletes the note \'<name\' from <player>.']
        }
    
    notesdict = {}
    try:
        with open('ClanNotesData.pickle', 'rb') as file:
            notesdict = pickle.load(file)
    except IOError:
        pass
    
    print('--Welcome to ClanNotesLite--')
    if (debug < 3):
        print('Debug Level: {}'.format(debug))
    print('Type \'help\' to list commands.')
    while True:
        main()
