import streamlit as st
from openai import OpenAI
from PIL import Image
import json
import base64


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="FairSplit AI",
    page_icon="💸",
    layout="wide"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f7f8fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2 {
    font-weight: 700 !important;
}

h3 {
    font-weight: 650 !important;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.item-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #eeeeee;
    margin-bottom: 12px;
}

.total-box {
    background: #111827;
    color: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
}

.person-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #eeeeee;
    margin-bottom: 10px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================

if "friends" not in st.session_state:
    st.session_state.friends = ["You"]

if "bill_data" not in st.session_state:
    st.session_state.bill_data = None

if "assignments" not in st.session_state:
    st.session_state.assignments = {}

if "split_result" not in st.session_state:
    st.session_state.split_result = None


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("👥 Friends")

    st.write("Add everyone who is sharing the bill.")

    new_friend = st.text_input(
        "Friend name",
        placeholder="e.g. Rahul"
    )

    if st.button("➕ Add Friend"):

        if new_friend.strip():

            name = new_friend.strip()

            if name not in st.session_state.friends:
                st.session_state.friends.append(name)
                st.success(f"{name} added!")

            else:
                st.warning("This friend already exists.")

    st.divider()

    st.subheader("Current Group")

    for i, friend in enumerate(st.session_state.friends):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"👤 {friend}")

        with col2:

            if friend != "You":

                if st.button("❌", key=f"remove_{i}"):

                    st.session_state.friends.remove(friend)

                    if friend in st.session_state.assignments:
                        del st.session_state.assignments[friend]

                    st.rerun()

    st.divider()

    st.info(
        "💡 Upload the bill, let AI read it, "
        "select who shared each item, and calculate the exact split."
    )


# =========================
# HEADER
# =========================

st.title("💸 FairSplit AI")

st.write(
    "Split your restaurant bill fairly — item by item."
)

st.divider()


# =========================
# UPLOAD BILL
# =========================

st.subheader("📸 1. Upload Your Bill")

uploaded_file = st.file_uploader(
    "Upload a clear photo of your restaurant bill",
    type=["jpg", "jpeg", "png"]
)


# =========================
# OPENAI SETUP
# =========================

try:

    api_key = st.secrets["OPENAI_API_KEY"]

    client = OpenAI(api_key=api_key)

except Exception:

    st.error(
        "OpenAI API key not found. Please add OPENAI_API_KEY "
        "inside .streamlit/secrets.toml"
    )

    st.stop()


# =========================
# ANALYZE BILL
# =========================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Bill",
        width=500
    )

    if st.button(
        "🔍 Analyze Bill with AI",
        type="primary"
    ):

        with st.spinner("AI is reading your bill..."):

            try:

                image_bytes = uploaded_file.getvalue()

                base64_image = base64.b64encode(
                    image_bytes
                ).decode("utf-8")

                mime_type = uploaded_file.type

                prompt = """
You are an expert restaurant bill parser.

Analyze the uploaded restaurant bill carefully.

Return ONLY valid JSON.

Use this exact structure:

{
    "restaurant_name": "string",
    "items": [
        {
            "name": "string",
            "quantity": 1,
            "price": 0.00
        }
    ],
    "subtotal": 0.00,
    "tax": 0.00,
    "service_charge": 0.00,
    "discount": 0.00,
    "total": 0.00
}

Rules:

1. Extract every food or drink item.
2. quantity must be numeric.
3. price must be the UNIT PRICE of the item.
4. Do not include subtotal, tax, service charge, discount or total as items.
5. If service charge is not present, use 0.
6. If discount is not present, use 0.
7. If tax is not present, use 0.
8. Preserve decimal prices accurately.
9. Read the final total carefully.
10. Return JSON only. No explanation.
"""

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    input=[
                        {
                            "role": "user",

                            "content": [

                                {
                                    "type": "input_text",
                                    "text": prompt
                                },

                                {
                                    "type": "input_image",
                                    "image_url":
                                    f"data:{mime_type};base64,{base64_image}"
                                }

                            ]
                        }
                    ]
                )

                result = response.output_text.strip()

                result = result.replace(
                    "```json",
                    ""
                ).replace(
                    "```",
                    ""
                ).strip()

                bill_data = json.loads(result)

                st.session_state.bill_data = bill_data

                st.session_state.assignments = {}

                st.session_state.split_result = None

                st.success("✅ Bill analyzed successfully!")

                st.rerun()

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# =========================
# SHOW BILL DATA
# =========================

if st.session_state.bill_data:

    bill = st.session_state.bill_data

    st.divider()

    st.subheader("🧾 2. Bill Details")

    st.markdown(
        f"""
        <div class="card">
            <h3>🏪 {bill.get("restaurant_name", "Restaurant")}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    items = bill.get("items", [])

    if not items:

        st.error("No items were detected in the bill.")

        st.stop()

    st.subheader("🍕 Items")

    for index, item in enumerate(items):

        name = item.get("name", "Unknown Item")
        quantity = float(item.get("quantity", 1))
        price = float(item.get("price", 0))

        item_total = quantity * price

        st.markdown(
            f"""
            <div class="item-card">

            <h4>{name}</h4>

            <p>
            Quantity: <b>{quantity:g}</b>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            Unit Price: <b>₹{price:.2f}</b>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            Item Total: <b>₹{item_total:.2f}</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =========================
    # BILL SUMMARY
    # =========================

    st.subheader("💰 Bill Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Subtotal",
            f"₹{float(bill.get('subtotal', 0)):.2f}"
        )

    with col2:
        st.metric(
            "Tax",
            f"₹{float(bill.get('tax', 0)):.2f}"
        )

    with col3:
        st.metric(
            "Service",
            f"₹{float(bill.get('service_charge', 0)):.2f}"
        )

    with col4:
        st.metric(
            "Discount",
            f"₹{float(bill.get('discount', 0)):.2f}"
        )

    with col5:
        st.metric(
            "TOTAL",
            f"₹{float(bill.get('total', 0)):.2f}"
        )


    # =========================
    # ITEM ASSIGNMENT
    # =========================

    st.divider()

    st.subheader("👥 3. Who Shared Each Item?")

    st.write(
        "Select everyone who had each item."
    )

    for index, item in enumerate(items):

        name = item.get("name", "Unknown Item")

        quantity = float(
            item.get("quantity", 1)
        )

        price = float(
            item.get("price", 0)
        )

        item_total = quantity * price

        st.markdown(
            f"### 🍽️ {name} — ₹{item_total:.2f}"
        )

        selected_people = []

        columns = st.columns(
            min(len(st.session_state.friends), 4)
        )

        for i, friend in enumerate(
            st.session_state.friends
        ):

            with columns[
                i % len(columns)
            ]:

                checked = st.checkbox(
                    friend,
                    key=f"item_{index}_{friend}"
                )

                if checked:
                    selected_people.append(friend)

        st.session_state.assignments[index] = selected_people

        if selected_people:

            st.caption(
                "Shared by: " +
                ", ".join(selected_people)
            )

        else:

            st.warning(
                "⚠️ Select at least one person."
            )


    # =========================
    # CALCULATE SPLIT
    # =========================

    st.divider()

    if st.button(
        "🧮 Calculate Exact Split",
        type="primary"
    ):

        invalid_items = []

        for index, item in enumerate(items):

            if not st.session_state.assignments.get(
                index
            ):

                invalid_items.append(
                    item.get("name", "Unknown Item")
                )

        if invalid_items:

            st.error(
                "Please select people for: "
                + ", ".join(invalid_items)
            )

        else:

            # -------------------------
            # ITEM TOTAL
            # -------------------------

            item_totals = []

            for item in items:

                quantity = float(
                    item.get("quantity", 1)
                )

                price = float(
                    item.get("price", 0)
                )

                item_total = quantity * price

                item_totals.append(
                    item_total
                )

            items_subtotal = sum(
                item_totals
            )

            tax = float(
                bill.get("tax", 0)
            )

            service_charge = float(
                bill.get("service_charge", 0)
            )

            discount = float(
                bill.get("discount", 0)
            )

            original_total = float(
                bill.get("total", 0)
            )

            # -------------------------
            # PERSON TOTALS
            # -------------------------

            person_totals = {
                friend: 0.0
                for friend in st.session_state.friends
            }

            person_items = {
                friend: []
                for friend in st.session_state.friends
            }

            # -------------------------
            # SPLIT ITEMS
            # -------------------------

            for index, item in enumerate(items):

                item_total = item_totals[index]

                people = st.session_state.assignments[
                    index
                ]

                share = (
                    item_total /
                    len(people)
                )

                for person in people:

                    person_totals[person] += share

                    person_items[person].append(
                        {
                            "name": item.get(
                                "name",
                                "Unknown Item"
                            ),
                            "amount": share
                        }
                    )


            # -------------------------
            # PROPORTIONAL TAX
            # -------------------------

            if items_subtotal > 0:

                for person in person_totals:

                    proportion = (
                        person_totals[person]
                        / items_subtotal
                    )

                    tax_share = (
                        tax * proportion
                    )

                    service_share = (
                        service_charge
                        * proportion
                    )

                    discount_share = (
                        discount
                        * proportion
                    )

                    person_totals[person] += (
                        tax_share
                        + service_share
                        - discount_share
                    )


            # -------------------------
            # ROUNDING
            # -------------------------

            person_totals = {
                person: round(
                    amount,
                    2
                )
                for person, amount
                in person_totals.items()
            }

            split_total = round(
                sum(person_totals.values()),
                2
            )

            difference = round(
                original_total - split_total,
                2
            )

            # Fix tiny rounding difference

            if abs(difference) <= 0.05:

                largest_person = max(
                    person_totals,
                    key=person_totals.get
                )

                person_totals[
                    largest_person
                ] = round(
                    person_totals[
                        largest_person
                    ] + difference,
                    2
                )

            st.session_state.split_result = {
                "person_totals":
                    person_totals,

                "person_items":
                    person_items,

                "original_total":
                    original_total,

                "split_total":
                    round(
                        sum(
                            person_totals.values()
                        ),
                        2
                    )
            }

            st.rerun()


# =========================
# RESULTS
# =========================

if st.session_state.split_result:

    result = st.session_state.split_result

    st.divider()

    st.subheader("💸 4. Who Owes What?")

    person_totals = result[
        "person_totals"
    ]

    person_items = result[
        "person_items"
    ]

    for person, amount in person_totals.items():

        with st.container():

            st.markdown(
                f"""
                <div class="person-box">

                <h3>👤 {person}</h3>

                <h2>₹{amount:.2f}</h2>

                </div>
                """,
                unsafe_allow_html=True
            )

            if person_items[person]:

                with st.expander(
                    f"View {person}'s items"
                ):

                    for item in person_items[person]:

                        st.write(
                            f"• {item['name']} "
                            f"— ₹{item['amount']:.2f}"
                        )


    # =========================
    # TOTAL VERIFICATION
    # =========================

    st.divider()

    original_total = result[
        "original_total"
    ]

    split_total = result[
        "split_total"
    ]

    difference = round(
        original_total - split_total,
        2
    )

    if abs(difference) <= 0.01:

        st.success(
            f"✅ Split verified! "
            f"₹{split_total:.2f} = "
            f"Original bill ₹{original_total:.2f}"
        )

    else:

        st.warning(
            f"⚠️ Small difference detected: "
            f"₹{difference:.2f}"
        )


    # =========================
    # SUMMARY
    # =========================

    st.markdown(
        f"""
        <div class="total-box">

        <h2>💰 Final Split</h2>

        <h1>₹{split_total:.2f}</h1>

        <p>
        Original Bill:
        ₹{original_total:.2f}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # RESET
    # =========================

    st.write("")

    if st.button("🔄 Start New Bill"):

        st.session_state.bill_data = None

        st.session_state.assignments = {}

        st.session_state.split_result = None

        st.rerun()