import difflib

#refresher:
#https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm

    #####################################################################################################################
    #algorithm kmp_search:
    #                           input:
    #                               an array of characters, S (the text to be searched)
    #                               an array of characters, W (the word sought)
    #                           output:
    #                               an array of integers, P (positions in S at which W is found)
    #                               an integer, nP (number of positions)

    #                           define variables:
    #                               an integer, j ← 0 (the position of the current character in S)
    #                               an integer, k ← 0 (the position of the current character in W)
    #                               an array of integers, T (the table, computed elsewhere)

    #                           let nP ← 0

    #                           while j < length(S) do
    #                               if W[k] = S[j] then
    #                                   let j ← j + 1
    #                                   let k ← k + 1
    #                                   if k = length(W) then
    #                                       (occurrence found, if only first occurrence is needed, m may be returned here)
    #                                       let P[nP] ← j - k, nP ← nP + 1
    #                                       let k ← T[k] (T[length(W)] can't be -1)
    #                               else
    #                                   let k ← T[k]
    #                                   if k < 0 then
    #                                       let j ← j + 1
    #                                       let k ← k + 1
    #
    #########################################################################################################################


def main():
    print "main"
    #input
    string_1 = "SMCard"
    string_2 = "SMCards_Activated.wav"
    string_3 = "wav"
    string_4 = "activated"

    #output
    posFoundArray = []  #position in target list at which input was found
    nP = 0              #number of positions

    #variables 
    j = 0               #posiotn of current character in the target string
    k = 0               #postion of current character in the input string
    table = []          #the table

    #let nP = 0


    #compare 1 & 2
    print "comparing string_1: '",string_1,"' with string_2: '",string_2,"'"


if __name__ == '__main__':
    main()