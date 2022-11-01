import copy

# reference: http://www.ngiam.net/NRIC/NRIC_numbers.pdf

# algorithm for S series checksum

Slookup = {}
Slookup[10] = 'A'
Slookup[9] = 'B'
Slookup[8] = 'C'
Slookup[7] = 'D'
Slookup[6] = 'E'
Slookup[5] = 'F'
Slookup[4] = 'G'
Slookup[3] = 'H'
Slookup[2] = 'I'
Slookup[1] = 'Z'
Slookup[0] = 'J'

# d = (2d_1 + 7d_2 + 6d_3 + 5d_4 + 4d_5 + 3d_6 + 2d_7) mod 11
weights = [2, 7, 6, 5, 4, 3, 2]

def check_letter(digits):
    d = sum(p * q for p,q in zip(weights, digits)) % 11
    return Slookup[d]

# algorithm for F series checksum
# same as for S but with a different lookup table

Flookup = {}
Flookup[10] = 'K'
Flookup[9] = 'L'
Flookup[8] = 'M'
Flookup[7] = 'N'
Flookup[6] = 'P'
Flookup[5] = 'Q'
Flookup[4] = 'R'
Flookup[3] = 'T'
Flookup[2] = 'U'
Flookup[1] = 'W'
Flookup[0] = 'X'

# algorithm for T series checksum
# same as for S but lookup table is S cyclic shifted 4 downwards

# algorithm for G series checksum
# same as for F but lookup table is F cyclic shifted 4 downwards

def successor(digits):
    idx = len(digits) - 1
    digits[idx] += 1
    while idx >= 1 and digits[idx] > 9:
        digits[idx] -= 10
        digits[idx-1] += 1
        idx -= 1
    if digits[0] > 9:
        return False
    else:
        return True

def find_collision(digits):
    letter = check_letter(digits)
    for i in range(0,7):
        test = copy.copy(digits)
        for d in range(0,10):
            if d != digits[i]:
                test[i] = d
                if check_letter(test) == letter:
                    print(test, digits, letter)

def enumerate():
    curr = [0, 0, 0, 0, 0, 0 ,0]
    while successor(curr):
        print(check_letter(curr), curr)

enumerate()
