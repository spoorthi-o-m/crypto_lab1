#include <bits/stdc++.h>
using namespace std;

/*
    ============================================================
                        BIG INTEGER
    ============================================================

    Stores large positive integers in chunks of 9 decimal digits.

    Example:

    123456789123456789

    is stored as:

    {123456789, 123456789}

    The least significant chunk is stored first.
*/

class BigInteger {
  
public:
    static const int BASE = 1000000000;
    vector<int> digits;
    // Constructor for zero
    BigInteger() {
        digits.push_back(0);
    }


    // Constructor from long long
    BigInteger(long long number) {

        if (number == 0) {
            digits.push_back(0);
            return;
        }

        while (number > 0) {
            digits.push_back(number % BASE);
            number /= BASE;
        }
    }


    // Constructor from string
    BigInteger(string value) {

        for (int i = (int)value.length(); i > 0; i -= 9) {

            int start = max(0, i - 9);

            string chunk =
                value.substr(start, i - start);

            digits.push_back(stoi(chunk));
        }

        normalize();
    }


    // Remove unnecessary leading zero chunks
    void normalize() {

        while (
            digits.size() > 1 &&
            digits.back() == 0
        ) {
            digits.pop_back();
        }
    }


    // Print the number
    void print() const {

        cout << digits.back();

        for (
            int i = (int)digits.size() - 2;
            i >= 0;
            i--
        ) {

            cout
                << setw(9)
                << setfill('0')
                << digits[i];
        }
    }


    // Convert BigInteger to string
    string toString() const {

        stringstream output;

        output << digits.back();

        for (
            int i = (int)digits.size() - 2;
            i >= 0;
            i--
        ) {

            output
                << setw(9)
                << setfill('0')
                << digits[i];
        }

        return output.str();
    }


    /*
        Compare:

        1  -> this > other
        0  -> equal
        -1 -> this < other
    */

    int compare(const BigInteger& other) const {

        if (digits.size() > other.digits.size())
            return 1;

        if (digits.size() < other.digits.size())
            return -1;


        for (
            int i = (int)digits.size() - 1;
            i >= 0;
            i--
        ) {

            if (digits[i] > other.digits[i])
                return 1;

            if (digits[i] < other.digits[i])
                return -1;
        }

        return 0;
    }


    bool operator<(const BigInteger& other) const {
        return compare(other) < 0;
    }

    bool operator>(const BigInteger& other) const {
        return compare(other) > 0;
    }

    bool operator<=(const BigInteger& other) const {
        return compare(other) <= 0;
    }

    bool operator>=(const BigInteger& other) const {
        return compare(other) >= 0;
    }

    bool operator==(const BigInteger& other) const {
        return compare(other) == 0;
    }

    bool operator!=(const BigInteger& other) const {
        return compare(other) != 0;
    }


    // Check whether number is zero
    bool isZero() const {

        return
            digits.size() == 1 &&
            digits[0] == 0;
    }


    // Check whether number is odd
    bool isOdd() const {

        return digits[0] % 2 == 1;
    }


    /*
        ============================================================
                            ADDITION
        ============================================================
    */

    BigInteger add(const BigInteger& other) const {

        BigInteger result;

        result.digits.clear();

        long long carry = 0;

        int maximum =
            max(
                digits.size(),
                other.digits.size()
            );


        for (int i = 0; i < maximum || carry; i++) {

            long long sum = carry;

            if (i < (int)digits.size())
                sum += digits[i];

            if (i < (int)other.digits.size())
                sum += other.digits[i];


            result.digits.push_back(
                sum % BASE
            );

            carry = sum / BASE;
        }

        result.normalize();

        return result;
    }


    /*
        ============================================================
                        SUBTRACTION

        Assumption:
        this >= other
        ============================================================
    */

    BigInteger subtract(const BigInteger& other) const {

        BigInteger result;

        result.digits.clear();

        long long borrow = 0;


        for (int i = 0; i < (int)digits.size(); i++) {

            long long current =
                digits[i] - borrow;

            if (i < (int)other.digits.size())
                current -= other.digits[i];


            if (current < 0) {

                current += BASE;

                borrow = 1;

            } else {

                borrow = 0;
            }


            result.digits.push_back(current);
        }

        result.normalize();

        return result;
    }


    /*
        ============================================================
                        MULTIPLICATION
        ============================================================
    */

    BigInteger multiply(const BigInteger& other) const {

        BigInteger result;

        result.digits.assign(
            digits.size() +
            other.digits.size(),
            0
        );


        for (int i = 0; i < (int)digits.size(); i++) {

            long long carry = 0;


            for (
                int j = 0;
                j < (int)other.digits.size() || carry;
                j++
            ) {

                long long current =
                    result.digits[i + j]
                    +
                    carry;


                if (j < (int)other.digits.size()) {

                    current +=
                        1LL *
                        digits[i] *
                        other.digits[j];
                }


                result.digits[i + j] =
                    current % BASE;

                carry =
                    current / BASE;
            }
        }

        result.normalize();

        return result;
    }


    /*
        Multiply by a small integer.
    */

    BigInteger multiplySmall(long long number) const {

        BigInteger result;

        result.digits.clear();

        long long carry = 0;


        for (int value : digits) {

            long long current =
                1LL * value * number + carry;

            result.digits.push_back(
                current % BASE
            );

            carry =
                current / BASE;
        }


        while (carry > 0) {

            result.digits.push_back(
                carry % BASE
            );

            carry /= BASE;
        }


        result.normalize();

        return result;
    }


    /*
        ============================================================
                        DIVIDE BY 2
        ============================================================

        Needed for Square-and-Multiply.
    */

    BigInteger divideBy2() const {

        BigInteger result;

        result.digits.assign(
            digits.size(),
            0
        );


        long long remainder = 0;


        for (
            int i = (int)digits.size() - 1;
            i >= 0;
            i--
        ) {

            long long current =
                digits[i] +
                remainder * BASE;

            result.digits[i] =
                current / 2;

            remainder =
                current % 2;
        }


        result.normalize();

        return result;
    }


    /*
        ============================================================
                        MODULO USING REPEATED SUBTRACTION

        This is suitable for demonstrating the algorithms.

        For very large practical cryptographic workloads,
        a more advanced division algorithm would be preferred.
        ============================================================
    */

    BigInteger mod(const BigInteger& modulus) const {

        if (modulus.isZero()) {
            throw runtime_error(
                "Modulo by zero"
            );
        }


        BigInteger remainder = *this;


        if (remainder < modulus)
            return remainder;


        /*
            Binary-style subtraction using doubled modulus.
        */

        while (remainder >= modulus) {

            BigInteger multiple = modulus;

            BigInteger previous = modulus;


            while (true) {

                BigInteger doubled =
                    multiple.add(multiple);

                if (doubled > remainder)
                    break;

                previous = multiple;
                multiple = doubled;
            }


            remainder =
                remainder.subtract(previous);
        }

        return remainder;
    }


    /*
        ============================================================
                            OPERATORS
        ============================================================
    */

    BigInteger operator+(
        const BigInteger& other
    ) const {

        return add(other);
    }


    BigInteger operator-(
        const BigInteger& other
    ) const {

        return subtract(other);
    }


    BigInteger operator*(
        const BigInteger& other
    ) const {

        return multiply(other);
    }
};


/*
    ============================================================
                    SIGNED BIG INTEGER

    Extended Euclidean Algorithm can produce:

    x = negative
    y = positive

    So we need signs in addition to BigInteger magnitude.
    ============================================================
*/

class SignedBigInteger {
public:

    BigInteger magnitude;
    bool negative;


    SignedBigInteger() {

        magnitude = BigInteger(0);
        negative = false;
    }


    SignedBigInteger(
        BigInteger value,
        bool sign = false
    ) {

        magnitude = value;

        negative =
            sign && !value.isZero();
    }


    string toString() const {

        if (negative)
            return "-" + magnitude.toString();

        return magnitude.toString();
    }


    SignedBigInteger multiply(
        const BigInteger& value
    ) const {

        return SignedBigInteger(
            magnitude.multiply(value),
            negative
        );
    }


    SignedBigInteger subtract(
        const SignedBigInteger& other
    ) const {

        // Different signs → addition

        if (negative != other.negative) {

            BigInteger value =
                magnitude.add(other.magnitude);

            return SignedBigInteger(
                value,
                negative
            );
        }


        int comparison =
            magnitude.compare(
                other.magnitude
            );


        if (comparison == 0) {

            return SignedBigInteger();
        }


        if (comparison > 0) {

            BigInteger value =
                magnitude.subtract(
                    other.magnitude
                );

            return SignedBigInteger(
                value,
                negative
            );
        }


        BigInteger value =
            other.magnitude.subtract(
                magnitude
            );


        return SignedBigInteger(
            value,
            !negative
        );
    }
};


/*
    ============================================================
                            GCD
    ============================================================
*/

BigInteger gcd(
    BigInteger first,
    BigInteger second
) {

    while (!second.isZero()) {

        BigInteger remainder =
            first.mod(second);

        first = second;
        second = remainder;
    }

    return first;
}


/*
    ============================================================
                    EXTENDED EUCLIDEAN ALGORITHM

    Returns:

    gcd(a,b), x, y

    such that:

    ax + by = gcd(a,b)
    ============================================================
*/


struct ExtendedResult {

    BigInteger gcdValue;

    SignedBigInteger x;
    SignedBigInteger y;
};


/*
    We need quotient for Extended Euclid.

    This implementation finds quotient by repeated doubling.
*/

pair<BigInteger, BigInteger> divideAndRemainder(
    BigInteger dividend,
    const BigInteger& divisor
) {

    if (divisor.isZero()) {

        throw runtime_error(
            "Division by zero"
        );
    }


    BigInteger quotient(0);

    BigInteger remainder = dividend;


    while (remainder >= divisor) {

        BigInteger current = divisor;
        BigInteger factor(1);


        while (true) {

            BigInteger doubled =
                current.add(current);

            if (doubled > remainder)
                break;

            current = doubled;
            factor = factor.add(factor);
        }


        remainder =
            remainder.subtract(current);

        quotient =
            quotient.add(factor);
    }


    return {
        quotient,
        remainder
    };
}


ExtendedResult extendedGCD(
    BigInteger first,
    BigInteger second
) {

    BigInteger oldR = first;
    BigInteger currentR = second;


    SignedBigInteger oldX(
        BigInteger(1),
        false
    );

    SignedBigInteger currentX(
        BigInteger(0),
        false
    );


    SignedBigInteger oldY(
        BigInteger(0),
        false
    );

    SignedBigInteger currentY(
        BigInteger(1),
        false
    );


    while (!currentR.isZero()) {

        auto division =
            divideAndRemainder(
                oldR,
                currentR
            );


        BigInteger quotient =
            division.first;

        BigInteger remainder =
            division.second;


        oldR = currentR;
        currentR = remainder;


        SignedBigInteger temporaryX =
            oldX.subtract(
                currentX.multiply(quotient)
            );

        oldX = currentX;
        currentX = temporaryX;


        SignedBigInteger temporaryY =
            oldY.subtract(
                currentY.multiply(quotient)
            );

        oldY = currentY;
        currentY = temporaryY;
    }


    return {
        oldR,
        oldX,
        oldY
    };
}


/*
    ============================================================
                        MODULAR ADDITION
    ============================================================
*/

BigInteger modularAddition(
    BigInteger first,
    BigInteger second,
    BigInteger modulus
) {

    BigInteger sum =
        first.add(second);

    return sum.mod(modulus);
}


/*
    ============================================================
                    MODULAR MULTIPLICATION
    ============================================================
*/

BigInteger modularMultiplication(
    BigInteger first,
    BigInteger second,
    BigInteger modulus
) {

    BigInteger product =
        first.multiply(second);

    return product.mod(modulus);
}


/*
    ============================================================
                SQUARE AND MULTIPLY

    Computes:

    base^exponent mod modulus
    ============================================================
*/

BigInteger modularPower(
    BigInteger base,
    BigInteger exponent,
    BigInteger modulus
) {

    BigInteger result(1);

    base = base.mod(modulus);


    while (!exponent.isZero()) {

        if (exponent.isOdd()) {

            result =
                result.multiply(base)
                .mod(modulus);
        }


        base =
            base.multiply(base)
            .mod(modulus);


        exponent =
            exponent.divideBy2();
    }


    return result;
}


/*
    ============================================================
                    NAIVE EXPONENTIATION
    ============================================================
*/

BigInteger naivePower(
    BigInteger base,
    BigInteger exponent,
    BigInteger modulus
) {

    BigInteger result(1);

    BigInteger one(1);


    while (!exponent.isZero()) {

        result =
            result.multiply(base)
            .mod(modulus);

        exponent =
            exponent.subtract(one);
    }


    return result;
}


/*
    ============================================================
                        MODULAR INVERSE
    ============================================================

    Uses Extended Euclidean Algorithm.

    If:

    ax + my = 1

    then:

    ax ≡ 1 (mod m)

    Therefore x is the modular inverse.
*/

string modularInverse(
    BigInteger number,
    BigInteger modulus
) {

    ExtendedResult answer =
        extendedGCD(
            number,
            modulus
        );


    if (answer.gcdValue != BigInteger(1)) {

        return "NO_INVERSE";
    }


    SignedBigInteger x = answer.x;


    if (!x.negative) {

        return
            x.magnitude.mod(modulus)
            .toString();
    }


    /*
        For negative x:

        -x mod m

        is equivalent to:

        m - (x mod m)
    */

    BigInteger remainder =
        x.magnitude.mod(modulus);


    if (remainder.isZero())
        return "0";


    return
        modulus.subtract(remainder)
        .toString();
}


/*
    ============================================================
                            MAIN

    Command format:

    crypto.exe gcd A B

    crypto.exe extgcd A B

    crypto.exe inverse A M

    crypto.exe modadd A B M

    crypto.exe modmul A B M

    crypto.exe modpow BASE EXPONENT MODULUS

    crypto.exe naivepow BASE EXPONENT MODULUS
    ============================================================
*/

int main(
    int argc,
    char* argv[]
) {

    try {

        if (argc < 2) {

            cout
                << "ERROR: No operation provided";

            return 1;
        }


        string operation = argv[1];


        /*
            ========================
                    GCD
            ========================
        */

        if (operation == "gcd") {

            if (argc != 4)
                throw runtime_error(
                    "Usage: gcd A B"
                );


            BigInteger first(argv[2]);
            BigInteger second(argv[3]);


            BigInteger answer =
                gcd(first, second);


            cout << answer.toString();
        }


        /*
            ========================
                EXTENDED GCD
            ========================
        */

        else if (operation == "extgcd") {

            if (argc != 4)
                throw runtime_error(
                    "Usage: extgcd A B"
                );


            BigInteger first(argv[2]);
            BigInteger second(argv[3]);


            ExtendedResult answer =
                extendedGCD(
                    first,
                    second
                );


            cout
                << "GCD="
                << answer.gcdValue.toString()
                << "\n";


            cout
                << "X="
                << answer.x.toString()
                << "\n";


            cout
                << "Y="
                << answer.y.toString();
        }


        /*
            ========================
                MODULAR INVERSE
            ========================
        */

        else if (operation == "inverse") {

            if (argc != 4)
                throw runtime_error(
                    "Usage: inverse A M"
                );


            BigInteger number(argv[2]);
            BigInteger modulus(argv[3]);


            cout
                << modularInverse(
                    number,
                    modulus
                );
        }


        /*
            ========================
                MODULAR ADDITION
            ========================
        */

        else if (operation == "modadd") {

            if (argc != 5)
                throw runtime_error(
                    "Usage: modadd A B M"
                );


            BigInteger first(argv[2]);
            BigInteger second(argv[3]);
            BigInteger modulus(argv[4]);


            cout
                << modularAddition(
                    first,
                    second,
                    modulus
                )
                .toString();
        }


        /*
            ========================
            MODULAR MULTIPLICATION
            ========================
        */

        else if (operation == "modmul") {

            if (argc != 5)
                throw runtime_error(
                    "Usage: modmul A B M"
                );


            BigInteger first(argv[2]);
            BigInteger second(argv[3]);
            BigInteger modulus(argv[4]);


            cout
                << modularMultiplication(
                    first,
                    second,
                    modulus
                )
                .toString();
        }


        /*
            ========================
            SQUARE AND MULTIPLY
            ========================
        */

        else if (operation == "modpow") {

            if (argc != 5)
                throw runtime_error(
                    "Usage: modpow BASE EXPONENT MODULUS"
                );


            BigInteger base(argv[2]);
            BigInteger exponent(argv[3]);
            BigInteger modulus(argv[4]);


            cout
                << modularPower(
                    base,
                    exponent,
                    modulus
                )
                .toString();
        }


        /*
            ========================
            NAIVE EXPONENTIATION
            ========================
        */

        else if (operation == "naivepow") {

            if (argc != 5)
                throw runtime_error(
                    "Usage: naivepow BASE EXPONENT MODULUS"
                );


            BigInteger base(argv[2]);
            BigInteger exponent(argv[3]);
            BigInteger modulus(argv[4]);


            cout
                << naivePower(
                    base,
                    exponent,
                    modulus
                )
                .toString();
        }


        else {

            cout
                << "ERROR: Unknown operation";

            return 1;
        }
    }


    catch (const exception& error) {

        cout
            << "ERROR: "
            << error.what();

        return 1;
    }


    return 0;
}