pa_list = open("./paList.txt", "r").read().split()
ag_list = open('./agList.txt', 'r').read().split()

import random
def calc_best_remaining(possible_words, remaining_words, printable=False, need_percentage=False, future_guesses=1):
    words_score = {}
    percentage_score = {}
    best_score = 100
    for x in possible_words:
        score_dict = calc_score_dict(x, remaining_words)

        # while future_guesses != 1:
        #     future_guesses -= 1
        #     for score in score_dict:
        #         for word in possible_words:
        #             new_score_dict = calc_score_dict(word, score_dict[score])

        final_score = 0
        for l in score_dict.values():
            final_score += len(l)**2
        final_score /= len(remaining_words)
        if final_score < best_score:
            best_score = final_score
        if final_score == best_score or set_mode == 'full_rank':
            words_score[x] = final_score
    if need_percentage:
        for k in words_score:
            percentage_score[k] = best_score/words_score[k]*100
    if printable:
        print(possible_words, words_score, score_dict)
    final = dict(sorted(words_score.items(), key=lambda item: item[1]))
    # if two_words == 0:
    if need_percentage:
        return final, percentage_score
    else:
        return final
    # else:
    #     p = 0
    #     words_score = {}
    #     percentage_score = {}
    #     best_score = 100
    #     calculated_nums = 0
    #     for f in final.keys(): # ['words']
    #         calculated_nums += 1
    #         print(f, calculated_nums)
    #         for x in possible_words:
    #             final_score = 0
    #             score_dict = {}
    #             for y in remaining_words:
    #                 score_list = [['0', '0'], ['0', '0'], ['0', '0'], ['0', '0'], ['0', '0']]
    #                 for a, b, c, n in zip(f, x, y, range(5)):
    #                     if a == c:
    #                         score_list[n][0] = '2'
    #                     elif a in y:
    #                         score_list[n][0] = '1'
    #                     if b == c:
    #                         score_list[n][1] = '2'
    #                     elif b in y:
    #                         score_list[n][1] = '1'
    #                 score = []
    #                 for i in score_list:
    #                     for j in i:
    #                         score.append(j)
    #                 score = ''.join(score)
    #                 if score not in score_dict:
    #                     score_dict[score] = 1
    #                 else:
    #                     score_dict[score] += 1
    #             for l in score_dict.values():
    #                 final_score += l**2
    #             final_score /= sum(score_dict.values())
    #             if final_score < best_score:
    #                 best_score = final_score
    #             words_score[f+'-'+x] = final_score
    #         if f in possible_words:
    #             possible_words.remove(f)
    #         p += 1
    #         if p == two_words:
    #             break
    #     for k in words_score:
    #         percentage_score[k] = best_score / words_score[k] * 100
    #     if printable:
    #         print(possible_words, words_score, score_dict)
    #     final = dict(sorted(words_score.items(), key=lambda item: item[1]))
    #     while len(final) > 1000:
    #         final.popitem()
    #     return final, percentage_score

def calc_score_dict(word, remaining_words):
    score_dict = {}
    for y in remaining_words:
        score = calc_score(word, y)
        score = ''.join(score)
        if score not in score_dict:
            score_dict[score] = [y]
        else:
            score_dict[score] += [y]
    return score_dict

def calc_score(word, answer):
    yellow_letters = calc_yellow_and_green(word, answer)
    score = ['0', '0', '0', '0', '0']  # ['0','0','0','0','0']
    for a, b, c in zip(word, answer, range(5)):
        if a == b:
            score[c] = '2'
        elif a in answer and a in yellow_letters:
            score[c] = '1'
            yellow_letters.remove(a)
    return score

def calc_yellow_and_green(word, answer, need_green=False):
    green_letters = []
    yellow_letters = []
    for a, b in zip(word, answer):
        if a == b:
            green_letters.append(a)
            if green_letters.count(a) + yellow_letters.count(a) > answer.count(a):
                yellow_letters.remove(a)
        elif a in answer:
            if green_letters.count(a) + yellow_letters.count(a) < answer.count(a):
                yellow_letters.append(a)
    if need_green:
        return yellow_letters, green_letters
    else:
        return yellow_letters

def FullRank():
    remaining_words = pa_list+ag_list
    final, percentage_score = calc_best_remaining(remaining_words, pa_list, need_percentage=True)
    ranking = 0
    for k in final:
        ranking += 1
        print(ranking, k, round(final[k], 3), round(percentage_score[k], 2))

def CalcGame(): # 00010, 00020, 00000 
    solo_word = True # Game config
    hard_mode = False # Game config
    answers = []
    if solo_word:
        answers.append(random.choice(pa_list))
        # answers = ['mourn'] # Game config
    else:
        answers = pa_list
        shit_dict = {}
        attempts_score = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
    for answer in answers:
        if solo_word:
            print("Answer:", answer)
        attempts = 1
        words_score = {}
        crt_list = pa_list
        starting_words = ['march'] # Game config
        start_word = 1
        last_word = starting_words[0]
        game_end = False
        while not game_end:
            score = calc_score(last_word, answer)
            remaining_words = []
            for k in crt_list:
                valid = True
                for a, b, c in zip(last_word, k, score):
                    if c == '0' and (a == b or k.count(a) >= last_word.count(a)) or c == '1' and (a not in k or a == b) or c == '2' and a != b: #k.count(a) >= last_word.count(a)  or a not in answer and a in k
                        valid = False
                        break
                if valid:
                    remaining_words.append(k)
            if solo_word:
                print(last_word, len(remaining_words), remaining_words)
            if hard_mode:
                all_words = remaining_words
            else:
                all_words = pa_list+ag_list
            if len(starting_words) > start_word:
                last_word = starting_words[start_word]
                start_word += 1
            elif len(remaining_words) > 2:
                final = calc_best_remaining(all_words, remaining_words)
                if solo_word and hard_mode:
                    print(final)
                for k in final:
                    last_word = k
                    best_score = final[k]
                    break
                for k in final:
                    if final[k] == best_score:
                        if k in remaining_words:
                            last_word = k
                            break
                    else:
                        break
            else:
                last_word = remaining_words[0]
            attempts += 1
            if last_word == answer:
                game_end = True
            else:
                crt_list = remaining_words
        if not solo_word:
            print(answer, attempts)
            if attempts < 7:
                attempts_score[str(attempts)] += 1
            else:
                shit_dict[last_word] = attempts
    if solo_word:
        print(last_word, answer, attempts)
    else:
        print(attempts_score)
        print(shit_dict)
        average_attempts = 0
        for k, l in zip(attempts_score.keys(), attempts_score.values()):
            average_attempts += (l/sum(attempts_score.values())) * int(k) #l*k/sum(attempts_score.values())
        print(round(average_attempts, 4))

def GetInput():
    # import time
    from termcolor import cprint
    random_first_word = False # Game config
    answer = random.choice(pa_list)
    attempts = 6
    game_end = False
    print('')
    print('\t', attempts, '| - - - - -', end=' ')
    while not game_end and attempts != 0:
        if not random_first_word or attempts != 6:
            player_word = input('| guess: ')
        else:
            player_word = random.choice(pa_list+ag_list)
            print('| guess:', player_word)
        if player_word in pa_list+ag_list:
            attempts -= 1
            print('\t', attempts, end=' | ')
            yellow_letters = calc_yellow_and_green(player_word, answer)
            for a, b in zip(player_word, answer):
                if a == b:
                    cprint(a, 'green', end=' ')
                elif a in answer and a in yellow_letters:
                    cprint(a, 'yellow', end=' ')
                    yellow_letters.remove(a)
                else:
                    print(a, end=' ')
            if player_word == answer:
                game_end = True
        else:
            print('\t', attempts, '| - - - - -', end=' ')
    if game_end:
        cprint('\n\n\tYou won!', 'green')
    else:
        cprint('\n\n\tYou lost!', 'red')
        print('\tAnswer: ', end='')
        cprint(answer, 'green')

def GetCheat():
    answer = 'plate' # Game Config
    anagrams = {}
    # second_chance = False
    while len(anagrams) == 0:
        for word in pa_list+ag_list:
            yellow_letters, green_letters = calc_yellow_and_green(word, answer, need_green=True)
            if len(yellow_letters)+len(green_letters) >= 4 and len(yellow_letters)+len(green_letters) != 5:
                if str(len(yellow_letters))+'y'+str(len(green_letters))+'g' not in anagrams:
                    anagrams[str(len(yellow_letters))+'y'+str(len(green_letters))+'g'] = [word]
                else:
                    anagrams[str(len(yellow_letters))+'y'+str(len(green_letters))+'g'] += [word]
    for i in anagrams:
        print(i, len(anagrams[i]), anagrams[i])

modes = ['input', 'calc_game', 'cheat', 'full_rank']
set_mode = modes[0]
if set_mode == 'full_rank':
    FullRank()
elif set_mode == 'calc_game':
    CalcGame()
elif set_mode == 'input':
    while True:
        GetInput()
        if input('\n\tPlay Again? [Y] [N] ').upper() != 'Y':
            break
elif set_mode == 'cheat':
    GetCheat()