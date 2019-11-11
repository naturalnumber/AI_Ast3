class ObjectiveFunction:
    def __init__(self, size, queens, rooks, bishops):
        self.size = size
        self.queens = queens
        self.rooks = rooks
        self.bishops = bishops
        self.total_pieces = queens+rooks+bishops

    def evaluate(self, x_arr, y_arr, type_arr):
        result = 0
        # for each piece
        for i in range(len(x_arr)):
            # we check if it is being attacked by another piece
            for j in range(len(x_arr)):
                if (i!=j) and (type_arr[j]<=1) and (x_arr[j]==x_arr[i] or y_arr[j]==y_arr[i]): # checking rows and columns for Queens and and Rooks
                    result+=1
                    break
                if (i!=j) and (type_arr[j]%2==0) and (abs(x_arr[j]-x_arr[i])==abs(y_arr[j]-y_arr[i])): # checking diagonals for Queens and Bishops
                    result+=1
                    break
        return result

    def check_constraints(self, x_arr, y_arr, type_arr):
        count_pieces = [0, 0, 0]     

        try:
            for i in range(len(x_arr)): 
                if x_arr[i]>self.size or x_arr[i]<1 or y_arr[i]>self.size or y_arr[i]<1: # if ome piece is outside the board
                    return False

                if type_arr[i] < 0 or type_arr[i] > 2: # if it is not a valid type
                    return False
                else:
                    count_pieces[type_arr[i]] += 1      # counting the number of pieces of each type
                
                for j in range(i+1, len(x_arr)):
                    if x_arr[i]==x_arr[j] and y_arr[i]==y_arr[j]: # if two pieces are in the same square
                        return False
        except:
            return False        # if anything goes wrong (out of bound) then it is not a valid solution
            
        if count_pieces[0]!=self.queens or count_pieces[1]!=self.rooks or count_pieces[2]!=self.bishops: # if the type count doesn't match the objective function count
            return False

        return True

             
