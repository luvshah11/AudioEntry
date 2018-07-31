import difflib

#refresher:
#https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
    #####################################################################################################################
    #algorithm kmp_table:
     #                          input:
     #                              an array of characters, W (the word to be analyzed)
     #                              an array of integers, T (the table to be filled)
     #                          output:
     #                              nothing (but during operation, it populates the table)
     #
     #                          define variables:
     #                              an integer, pos = 1 (the current position we are computing in T)
     #                              an integer, cnd = 0 (the zero-based index in W of the next character of the current candidate substring)
     #
     #                          let T[0] = -1
     #
     #                          while pos < length(W) do
     #                              if W[pos] = W[cnd] then
     #                                  let T[pos] = T[cnd], pos = pos + 1, cnd = cnd + 1
     #                              else
     #                                  let T[pos] = cnd
     #
     #                                  let cnd = T[cnd] (to increase performance)
     #
     #                                  while cnd >= 0 and W[pos] <> W[cnd] do
     #                                      let cnd = T[cnd]
     #
     #                                  let pos = pos + 1, cnd = cnd + 1
     #
     #                          let T[pos] = cnd (only need when all word occurrences searched)
     #
    #####################################################################################################################
    #algorithm kmp_search:
    #                           input:
    #                               an array of characters, S (the text to be searched)
    #                               an array of characters, W (the word sought)
    #                           output:
    #                               an array of integers, P (positions in S at which W is found)
    #                               an integer, nP (number of positions)

    #                           define variables:
    #                               an integer, j = 0 (the position of the current character in S)
    #                               an integer, k = 0 (the position of the current character in W)
    #                               an array of integers, T (the table, computed elsewhere)

    #                           let nP = 0

    #                           while j < length(S) do
    #                               if W[k] = S[j] then
    #                                   let j = j + 1
    #                                   let k = k + 1
    #                                   if k = length(W) then
    #                                       (occurrence found, if only first occurrence is needed, m may be returned here)
    #                                       let P[nP] = j - k, nP = nP + 1
    #                                       let k = T[k] (T[length(W)] can't be -1)
    #                               else
    #                                   let k = T[k]
    #                                   if k < 0 then
    #                                       let j = j + 1
    #                                       let k = k + 1
    #
    #########################################################################################################################
    # complexity O(n)


def build_KMP_table(string_in):
    #input:
    string_in   #    an array of characters, W (the word to be analyzed)
    T  = list()     #    an array of integers, T (the table to be filled)
    
    #define variables:
    pos = 1    #an integer, pos = 1 (the current position we are computing in T)
    cnd = 0    #an integer, cnd = 0 (the zero-based index in W of the next character of the current candidate substring)

    T[0] = -1

    while pos < len(string_in):
        if(string_in[pos] == string_in[cnd]):
            T[pos] = T[cnd]
            pos = pos + 1
            cnd = cnd + 1
        else:
            T[pos] = cnd
            cnd = T[cnd]
            while cnd >= 0 and string_in[pos] != string_in[cnd]:
                cnd = T[cnd]
            pos = pos + 1
            cnd = cnd + 1
        T[pos] = cnd
    return T

def KMP_algo(text, pattern):

    # allow indexing into pattern and protect against change during yield
    text = text.lower()
    pattern = pattern.lower()
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            return  startPos

def main():
    print "main"

    #input
    string_1 = "SMCard"
    string_2 = "SMCards_Activated.wav"
    string_3 = "wav"
    string_4 = "Activated"

    print  KMP_algo(string_2, string_4)

if __name__ == '__main__':
    main()