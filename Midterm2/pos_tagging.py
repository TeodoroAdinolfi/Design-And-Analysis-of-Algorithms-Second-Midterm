def pos_tagging(R, S, T, E):
    m,n = len(R),len(S)
    # Declare a void matrix of size m*n where m is the number of tags and n is the number of words
    mat = [[(0,0)]*(n) for k in range(m)]
    maxVal = 0
    maxIndex = 0
    # Fill the dynamic matrix
    for j in range(n):
        for i in range(m):
            if (j == 0):
                #Boundary condition: first word probability is given by the transition from start the word we are considering
                #assouming that the given word has a certain role
                mat[i][j] = T["Start"][R[i]]*E[S[0]][R[i]],0
            elif(j == n-1):
                #Last word must consider that in addition to the probability calculeted in all the other case must be considered the trnasition from
                # that word to the end (given that we know that is the last word of the sentence)
                maxVal,maxIndex =  __argMax(mat,j-1,m,T,R,R[i])
                mat[i][j] =maxVal*T[R[i]]["End"]*E[S[j]][R[i]],maxIndex            
            else:
                #In the genral case we have to consider that the higer probability for the word S[i] in the role R[j] is given by the probability that
                #the word S[j] has the role R[i] multiplied by the probability that the word S[j-1] has the role R[maxIndex] (the role that maximizes the total probability calculated in the previous step)
                maxVal,maxIndex =  __argMax(mat,j-1,m,T,R,R[i]) 
                mat[i][j] = maxVal*E[S[j]][R[i]],maxIndex
    tags = dict()
    #Backtracking to find the best path
    #Find the last word with the highest probability
    maxVal = (mat[0][n-1])[0]
    lastMax = 0
    for k in range(1,m):
        if  (mat[k][n-1])[0] > maxVal:
            lastMax = k
            maxVal = (mat[k][n-1])[0]
    tags[S[n-1]]=R[lastMax]
    #Find the other words in the path by using the index stored with the previous word
    for i in range(n-1,-1,-1):
        lastMax= (mat[lastMax][i])[1] 
        tags[S[i-1]]=R[lastMax]

    return tags

#Function that returns the maximum value and the index of the maximum value in the column col of the matrix mat
def __argMax(mat,col,m,T,R,ri):
    max = (mat[0][col])[0] * T[R[0]][ri]
    index = 0
    for k in range(1,m):
        if  (mat[k][col])[0] * T[R[k]][ri] > max:
            index = k
            max = (mat[k][col])[0] * T[R[k]][ri]
    return max,index

