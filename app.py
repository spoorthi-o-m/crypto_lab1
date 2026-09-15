import streamlit as st
import subprocess
import os
import time
import math


# ============================================================
#                    PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cryptography Calculator",
    page_icon="🔐",
    layout="wide"
)


# ============================================================
#                         TITLE
# ============================================================

st.title("🔐 Cryptography Calculator")

st.write(
    """
    A calculator implementing fundamental cryptographic and
    number-theoretic algorithms using a custom C++ BigInteger
    implementation.
    """
)


# ============================================================
#                    FIND C++ EXECUTABLE
# ============================================================

CURRENT_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)

EXECUTABLE = os.path.join(
    CURRENT_FOLDER,
    "crypto.exe"
)


# ============================================================
#                      RUN C++ PROGRAM
# ============================================================

def run_cpp(arguments):

    command = [EXECUTABLE] + arguments

    start_time = time.perf_counter()

    process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    if process.returncode != 0:

        return (
            "ERROR: " + process.stdout.strip(),
            execution_time
        )

    return (
        process.stdout.strip(),
        execution_time
    )


# ============================================================
#                   EXTENDED GCD FOR VERIFICATION
# ============================================================

def python_extended_gcd(a, b):

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:

        quotient = old_r // r

        old_r, r = (
            r,
            old_r - quotient * r
        )

        old_s, s = (
            s,
            old_s - quotient * s
        )

        old_t, t = (
            t,
            old_t - quotient * t
        )

    return old_r, old_s, old_t


# ============================================================
#                   DISPLAY VERIFICATION
# ============================================================

def show_verification(
    custom_answer,
    trusted_answer
):

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🔧 Custom C++ Implementation"
        )

        st.code(
            str(custom_answer)
        )

    with right:

        st.subheader(
            "📚 Trusted Python Implementation"
        )

        st.code(
            str(trusted_answer)
        )

    if (
        str(custom_answer).strip()
        ==
        str(trusted_answer).strip()
    ):

        st.success(
            "✅ VERIFIED: Both implementations produced the same result."
        )

    else:

        st.error(
            "❌ VERIFICATION FAILED: Results do not match."
        )


# ============================================================
#                       SIDEBAR
# ============================================================

st.sidebar.title("🔐 Calculator Menu")


operation = st.sidebar.radio(

    "Choose an Operation",

    [

        "GCD",

        "Extended GCD",

        "Find x and y",

        "Modular Inverse",

        "Modular Addition",

        "Modular Multiplication",

        "Modular Exponentiation",

        "Verification"
    ]
)


# ============================================================
#                            GCD
# ============================================================

if operation == "GCD":

    st.header("📐 Euclidean GCD")

    st.latex(
        r"\gcd(a,b)"
    )

    first, second = st.columns(2)

    with first:

        a = st.text_input(
            "Enter A",
            key="gcd_a"
        )

    with second:

        b = st.text_input(
            "Enter B",
            key="gcd_b"
        )

    if st.button(
        "Calculate GCD",
        use_container_width=True
    ):

        if a and b:

            answer, execution_time = run_cpp(

                [
                    "gcd",
                    a,
                    b
                ]
            )

            st.success(
                f"GCD = {answer}"
            )

            st.caption(
                f"Execution time: {execution_time:.6f} seconds"
            )

        else:

            st.warning(
                "Please enter both numbers."
            )


# ============================================================
#                       EXTENDED GCD
# ============================================================

elif operation == "Extended GCD":

    st.header("📐 Extended Euclidean Algorithm")

    st.latex(
        r"ax+by=\gcd(a,b)"
    )

    first, second = st.columns(2)

    with first:

        a = st.text_input(
            "Enter A",
            key="ext_a"
        )

    with second:

        b = st.text_input(
            "Enter B",
            key="ext_b"
        )

    if st.button(
        "Run Extended GCD",
        use_container_width=True
    ):

        if a and b:

            answer, execution_time = run_cpp(

                [
                    "extgcd",
                    a,
                    b
                ]
            )

            st.code(answer)

            st.caption(
                f"Execution time: {execution_time:.6f} seconds"
            )

        else:

            st.warning(
                "Please enter both numbers."
            )


# ============================================================
#                     FIND X AND Y
# ============================================================

elif operation == "Find x and y":

    st.header("🔢 Find Bézout Coefficients")

    st.write(
        """
        Find integers **x** and **y** satisfying:
        """
    )

    st.latex(
        r"ax+by=\gcd(a,b)"
    )

    first, second = st.columns(2)

    with first:

        a = st.text_input(
            "Enter A",
            key="xy_a"
        )

    with second:

        b = st.text_input(
            "Enter B",
            key="xy_b"
        )

    if st.button(
        "Find X and Y",
        use_container_width=True
    ):

        if a and b:

            answer, _ = run_cpp(

                [
                    "extgcd",
                    a,
                    b
                ]
            )

            st.subheader("Result")

            st.code(answer)

            lines = answer.split("\n")

            try:

                gcd_value = lines[0].split("=")[1]

                x_value = lines[1].split("=")[1]

                y_value = lines[2].split("=")[1]

                st.subheader(
                    "Mathematical Verification"
                )

                st.latex(

                    f"{a}({x_value})"

                    +

                    f"+ {b}({y_value})"

                    +

                    f"= {gcd_value}"
                )

            except:

                pass

        else:

            st.warning(
                "Please enter both numbers."
            )


# ============================================================
#                     MODULAR INVERSE
# ============================================================

elif operation == "Modular Inverse":

    st.header("🔄 Modular Inverse")

    st.latex(
        r"a^{-1}\pmod m"
    )

    first, second = st.columns(2)

    with first:

        a = st.text_input(
            "Enter A",
            key="inverse_a"
        )

    with second:

        modulus = st.text_input(
            "Enter Modulus M",
            key="inverse_m"
        )

    if st.button(
        "Find Modular Inverse",
        use_container_width=True
    ):

        if a and modulus:

            answer, execution_time = run_cpp(

                [
                    "inverse",
                    a,
                    modulus
                ]
            )

            if answer == "NO_INVERSE":

                st.error(
                    "❌ Modular inverse does not exist."
                )

            else:

                st.success(
                    f"Modular Inverse = {answer}"
                )

            st.caption(
                f"Execution time: {execution_time:.6f} seconds"
            )

        else:

            st.warning(
                "Please fill all fields."
            )


# ============================================================
#                    MODULAR ADDITION
# ============================================================

elif operation == "Modular Addition":

    st.header("➕ Modular Addition")

    st.latex(
        r"(a+b)\bmod m"
    )

    first, second, third = st.columns(3)

    with first:

        a = st.text_input(
            "Enter A",
            key="add_a"
        )

    with second:

        b = st.text_input(
            "Enter B",
            key="add_b"
        )

    with third:

        modulus = st.text_input(
            "Enter Modulus M",
            key="add_m"
        )

    if st.button(
        "Calculate Modular Addition",
        use_container_width=True
    ):

        if a and b and modulus:

            answer, execution_time = run_cpp(

                [
                    "modadd",
                    a,
                    b,
                    modulus
                ]
            )

            st.success(
                f"Result = {answer}"
            )

            st.caption(
                f"Execution time: {execution_time:.6f} seconds"
            )

        else:

            st.warning(
                "Please fill all fields."
            )


# ============================================================
#                 MODULAR MULTIPLICATION
# ============================================================

elif operation == "Modular Multiplication":

    st.header("✖️ Modular Multiplication")

    st.latex(
        r"(a\times b)\bmod m"
    )

    first, second, third = st.columns(3)

    with first:

        a = st.text_input(
            "Enter A",
            key="mul_a"
        )

    with second:

        b = st.text_input(
            "Enter B",
            key="mul_b"
        )

    with third:

        modulus = st.text_input(
            "Enter Modulus M",
            key="mul_m"
        )

    if st.button(
        "Calculate Modular Multiplication",
        use_container_width=True
    ):

        if a and b and modulus:

            answer, execution_time = run_cpp(

                [
                    "modmul",
                    a,
                    b,
                    modulus
                ]
            )

            st.success(
                f"Result = {answer}"
            )

            st.caption(
                f"Execution time: {execution_time:.6f} seconds"
            )

        else:

            st.warning(
                "Please fill all fields."
            )


# ============================================================
#                  MODULAR EXPONENTIATION
# ============================================================

elif operation == "Modular Exponentiation":

    st.header("⚡ Modular Exponentiation")

    st.write(
        """
        This experiment compares:

        - 🐢 Naive Exponentiation
        - ⚡ Square-and-Multiply
        """
    )

    first, second, third = st.columns(3)

    with first:

        base = st.text_input(
            "Enter Base",
            key="power_base"
        )

    with second:

        exponent = st.text_input(
            "Enter Exponent",
            key="power_exponent"
        )

    with third:

        modulus = st.text_input(
            "Enter Modulus",
            key="power_modulus"
        )

    if st.button(
        "Run Both Algorithms",
        use_container_width=True
    ):

        if base and exponent and modulus:

            # ----------------------------
            # Naive Method
            # ----------------------------

            naive_answer, naive_time = run_cpp(

                [
                    "naivepow",
                    base,
                    exponent,
                    modulus
                ]
            )

            # ----------------------------
            # Square and Multiply
            # ----------------------------

            fast_answer, fast_time = run_cpp(

                [
                    "modpow",
                    base,
                    exponent,
                    modulus
                ]
            )

            left, right = st.columns(2)

            with left:

                st.subheader(
                    "🐢 Naive Method"
                )

                st.code(naive_answer)

            with right:

                st.subheader(
                    "⚡ Square-and-Multiply"
                )

                st.code(fast_answer)

            # ----------------------------
            # Verify both answers
            # ----------------------------

            if naive_answer == fast_answer:

                st.success(
                    "✅ Both algorithms produced the same result."
                )

            else:

                st.error(
                    "❌ Results do not match."
                )

            # ----------------------------
            # Performance Comparison
            # ----------------------------

            st.subheader(
                "📊 Performance Comparison"
            )

            metric1, metric2, metric3 = st.columns(3)

            with metric1:

                st.metric(
                    "Naive Time",
                    f"{naive_time:.6f} sec"
                )

            with metric2:

                st.metric(
                    "Square-and-Multiply Time",
                    f"{fast_time:.6f} sec"
                )

            with metric3:

                if fast_time > 0:

                    speedup = (
                        naive_time /
                        fast_time
                    )

                    st.metric(
                        "Speed Improvement",
                        f"{speedup:.2f}×"
                    )

        else:

            st.warning(
                "Please fill all fields."
            )


# ============================================================
#                  TASK 7: VERIFICATION
# ============================================================

elif operation == "Verification":

    st.header(
        "✅ Task 7: Verification Against a Trusted Library"
    )

    st.write(
        """
        The custom C++ BigInteger implementation is independently
        checked against Python's arbitrary-precision integers and
        trusted mathematical operations.
        """
    )

    verification_operation = st.selectbox(

        "Choose an operation to verify",

        [

            "GCD",

            "Modular Addition",

            "Modular Multiplication",

            "Modular Inverse",

            "Modular Exponentiation",

            "Extended GCD"
        ]
    )


    # ========================================================
    # VERIFY GCD
    # ========================================================

    if verification_operation == "GCD":

        left, right = st.columns(2)

        with left:

            a = st.text_input(
                "Enter A",
                key="verify_gcd_a"
            )

        with right:

            b = st.text_input(
                "Enter B",
                key="verify_gcd_b"
            )

        if st.button("Verify GCD"):

            if a and b:

                custom_answer, _ = run_cpp(

                    [
                        "gcd",
                        a,
                        b
                    ]
                )

                trusted_answer = math.gcd(
                    int(a),
                    int(b)
                )

                show_verification(
                    custom_answer,
                    trusted_answer
                )


    # ========================================================
    # VERIFY MODULAR ADDITION
    # ========================================================

    elif verification_operation == "Modular Addition":

        a = st.text_input(
            "Enter A",
            key="verify_add_a"
        )

        b = st.text_input(
            "Enter B",
            key="verify_add_b"
        )

        modulus = st.text_input(
            "Enter M",
            key="verify_add_m"
        )

        if st.button(
            "Verify Modular Addition"
        ):

            if a and b and modulus:

                custom_answer, _ = run_cpp(

                    [
                        "modadd",
                        a,
                        b,
                        modulus
                    ]
                )

                trusted_answer = (
                    int(a) + int(b)
                ) % int(modulus)

                show_verification(
                    custom_answer,
                    trusted_answer
                )


    # ========================================================
    # VERIFY MODULAR MULTIPLICATION
    # ========================================================

    elif verification_operation == "Modular Multiplication":

        a = st.text_input(
            "Enter A",
            key="verify_mul_a"
        )

        b = st.text_input(
            "Enter B",
            key="verify_mul_b"
        )

        modulus = st.text_input(
            "Enter M",
            key="verify_mul_m"
        )

        if st.button(
            "Verify Modular Multiplication"
        ):

            if a and b and modulus:

                custom_answer, _ = run_cpp(

                    [
                        "modmul",
                        a,
                        b,
                        modulus
                    ]
                )

                trusted_answer = (
                    int(a) * int(b)
                ) % int(modulus)

                show_verification(
                    custom_answer,
                    trusted_answer
                )


    # ========================================================
    # VERIFY MODULAR INVERSE
    # ========================================================

    elif verification_operation == "Modular Inverse":

        a = st.text_input(
            "Enter A",
            key="verify_inverse_a"
        )

        modulus = st.text_input(
            "Enter Modulus M",
            key="verify_inverse_m"
        )

        if st.button(
            "Verify Modular Inverse"
        ):

            if a and modulus:

                custom_answer, _ = run_cpp(

                    [
                        "inverse",
                        a,
                        modulus
                    ]
                )

                try:

                    trusted_answer = pow(
                        int(a),
                        -1,
                        int(modulus)
                    )

                    show_verification(
                        custom_answer,
                        trusted_answer
                    )

                except ValueError:

                    st.warning(
                        "Python confirms that no modular inverse exists."
                    )


    # ========================================================
    # VERIFY MODULAR EXPONENTIATION
    # ========================================================

    elif verification_operation == "Modular Exponentiation":

        base = st.text_input(
            "Enter Base",
            key="verify_power_base"
        )

        exponent = st.text_input(
            "Enter Exponent",
            key="verify_power_exponent"
        )

        modulus = st.text_input(
            "Enter Modulus",
            key="verify_power_modulus"
        )

        if st.button(
            "Verify Modular Exponentiation"
        ):

            if base and exponent and modulus:

                custom_answer, _ = run_cpp(

                    [
                        "modpow",
                        base,
                        exponent,
                        modulus
                    ]
                )

                trusted_answer = pow(
                    int(base),
                    int(exponent),
                    int(modulus)
                )

                show_verification(
                    custom_answer,
                    trusted_answer
                )


    # ========================================================
    # VERIFY EXTENDED GCD
    # ========================================================

    elif verification_operation == "Extended GCD":

        a = st.text_input(
            "Enter A",
            key="verify_ext_a"
        )

        b = st.text_input(
            "Enter B",
            key="verify_ext_b"
        )

        if st.button(
            "Verify Extended GCD"
        ):

            if a and b:

                custom_answer, _ = run_cpp(

                    [
                        "extgcd",
                        a,
                        b
                    ]
                )

                lines = custom_answer.split("\n")

                try:

                    custom_gcd = int(
                        lines[0].split("=")[1]
                    )

                    custom_x = int(
                        lines[1].split("=")[1]
                    )

                    custom_y = int(
                        lines[2].split("=")[1]
                    )

                    trusted_gcd, trusted_x, trusted_y = (
                        python_extended_gcd(
                            int(a),
                            int(b)
                        )
                    )

                    equation_value = (

                        int(a) * custom_x

                        +

                        int(b) * custom_y
                    )

                    left, right = st.columns(2)

                    with left:

                        st.subheader(
                            "🔧 Custom C++"
                        )

                        st.code(
                            custom_answer
                        )

                    with right:

                        st.subheader(
                            "📚 Python Verification"
                        )

                        st.code(

                            f"GCD={trusted_gcd}\n"

                            f"X={trusted_x}\n"

                            f"Y={trusted_y}"
                        )

                    st.subheader(
                        "Mathematical Check"
                    )

                    st.latex(

                        f"{a}({custom_x})"

                        +

                        f"+ {b}({custom_y})"

                        +

                        f"= {equation_value}"
                    )

                    if (

                        equation_value == custom_gcd

                        and

                        custom_gcd == trusted_gcd
                    ):

                        st.success(
                            """
                            ✅ VERIFIED!

                            The C++ Bézout coefficients satisfy:

                            ax + by = gcd(a,b)
                            """
                        )

                    else:

                        st.error(
                            "❌ Verification failed."
                        )

                except Exception as error:

                    st.error(
                        f"Could not verify output: {error}"
                    )


# ============================================================
#                           FOOTER
# ============================================================

st.divider()

st.caption(
    """
    Cryptography Lab 1 —
    Modular Arithmetic and Extended Euclidean Algorithm
    """
)