"""
iPhone Order System - Streamlit Web Application
Developer: Nick Ward
"""

import streamlit as st
import datetime
import os

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "order_history.txt")
MENU_FILE = os.path.join(SCRIPT_DIR, "menu.txt")
HUMAN_REPORT = os.path.join(SCRIPT_DIR, "latest_receipt.txt")

# Pricing configuration
PRICES = {
    "Standard": 799,
    "Plus": 899,
    "Pro": 999,
    "Pro Max": 1199
}

STORAGE_PRICES = {
    "128GB": 0,
    "256GB": 100,
    "512GB": 300,
    "1TB": 500
}

ADDON_PRICES = {
    "AppleCare+": 199,
    "Fast Charger": 29
}


# ======================== HELPER FUNCTIONS ========================

def load_menu():
    """Return menu options"""
    return {
        "MODEL": ["Standard", "Plus", "Pro", "Pro Max"],
        "STORAGE": ["128GB", "256GB", "512GB", "1TB"],
        "COLOR": ["Black", "Silver", "Blue", "Gold", "Purple"],
        "APPLECARE": ["Yes", "No"],
        "CHARGER": ["Yes", "No"]
    }


def load_orders():
    """Load all orders from order_history.txt"""
    orders = []
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 11:
                        order_dict = {
                            "timestamp": parts[0],
                            "first_name": parts[1],
                            "last_name": parts[2],
                            "phone_number": parts[3],
                            "address": parts[4],
                            "model": parts[5],
                            "storage": parts[6],
                            "color": parts[7],
                            "applecare": parts[8],
                            "charger": parts[9],
                            "total": float(parts[10])
                        }
                        orders.append(order_dict)
    except FileNotFoundError:
        pass
    return orders


def get_recent_orders(n=5):
    """Get the n most recent orders"""
    orders = load_orders()
    return sorted(orders, key=lambda x: x["timestamp"], reverse=True)[:n]


def calculate_total(model, storage, applecare, charger):
    """Calculate order total based on selections"""
    base_price = PRICES.get(model, 999)
    storage_cost = STORAGE_PRICES.get(storage, 0)
    
    total = base_price + storage_cost
    
    if applecare == "Yes":
        total += ADDON_PRICES["AppleCare+"]
    if charger == "Yes":
        total += ADDON_PRICES["Fast Charger"]
    
    return total


def save_order(first_name, last_name, phone_number, address, model, storage, color, applecare, charger, total):
    """Save order to order_history.txt"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(DATA_FILE, "a") as file:
        file.write(f"{timestamp}|{first_name}|{last_name}|{phone_number}|{address}|{model}|{storage}|{color}|{applecare}|{charger}|{total:.2f}\n")
    
    # Save receipt
    with open(HUMAN_REPORT, "w") as file:
        file.write(f"Receipt - {timestamp}\n")
        file.write(f"{first_name} {last_name} | {address}\n")
        file.write(f"Phone Number: {phone_number}\n\n")
        file.write(f"Model: {model}\n")
        file.write(f"Storage: {storage}\n")
        file.write(f"Color: {color}\n")
        file.write(f"AppleCare+: {applecare}\n")
        file.write(f"Charger: {charger}\n\n")
        file.write(f"Total: ${total:.2f}\n")
        file.write("------------------\n")


def update_order(order_index, model, storage, color, applecare, charger):
    """Update an existing order"""
    orders = load_orders()
    
    if order_index >= len(orders):
        st.error("Order not found!")
        return
    
    order = orders[order_index]
    total = calculate_total(model, storage, applecare, charger)
    
    # Update the order
    order["model"] = model
    order["storage"] = storage
    order["color"] = color
    order["applecare"] = applecare
    order["charger"] = charger
    order["total"] = total
    
    # Rewrite the entire file
    with open(DATA_FILE, "w") as file:
        for o in orders:
            file.write(f"{o['timestamp']}|{o['first_name']}|{o['last_name']}|{o['phone_number']}|{o['address']}|{o['model']}|{o['storage']}|{o['color']}|{o['applecare']}|{o['charger']}|{o['total']:.2f}\n")
    
    st.success("Order updated successfully!")


def delete_order(order_index):
    """Delete an existing order"""
    orders = load_orders()
    
    if order_index >= len(orders):
        st.error("Order not found!")
        return
    
    # Remove the order
    orders.pop(order_index)
    
    # Rewrite the entire file
    with open(DATA_FILE, "w") as file:
        for o in orders:
            file.write(f"{o['timestamp']}|{o['first_name']}|{o['last_name']}|{o['phone_number']}|{o['address']}|{o['model']}|{o['storage']}|{o['color']}|{o['applecare']}|{o['charger']}|{o['total']:.2f}\n")
    
    st.success("Order deleted successfully!")


# ======================== SESSION STATE INITIALIZATION ========================

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.user_first_name = ""
    st.session_state.user_last_name = ""
    st.session_state.user_phone_number = ""


# ======================== SIDEBAR - USER LOGIN/CREATION ========================

st.sidebar.title("User Account")

if not st.session_state.user_logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Create Account"])
    
    with tab1:
        st.subheader("Login")
        login_first = st.text_input("First Name", key="login_first")
        login_last = st.text_input("Last Name", key="login_last")
        login_phone = st.text_input("Phone Number", key="login_phone")
        
        if st.button("Login"):
            if login_first and login_last and login_phone:
                st.session_state.user_logged_in = True
                st.session_state.user_first_name = login_first.title()
                st.session_state.user_last_name = login_last.title()
                st.session_state.user_phone_number = login_phone
                st.success(f"Welcome, {st.session_state.user_first_name}!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create Account")
        create_first = st.text_input("First Name", key="create_first")
        create_last = st.text_input("Last Name", key="create_last")
        create_phone = st.text_input("Phone Number", key="create_phone")
        
        if st.button("Create Account"):
            if create_first and create_last and create_phone:
                st.session_state.user_logged_in = True
                st.session_state.user_first_name = create_first.title()
                st.session_state.user_last_name = create_last.title()
                st.session_state.user_phone_number = create_phone
                st.success(f"Account created! Welcome, {st.session_state.user_first_name}!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
else:
    st.sidebar.write(f"**Logged in as:**")
    st.sidebar.write(f"{st.session_state.user_first_name} {st.session_state.user_last_name}")
    st.sidebar.write(f"Phone: {st.session_state.user_phone_number}")
    
    if st.sidebar.button("Logout"):
        st.session_state.user_logged_in = False
        st.session_state.user_first_name = ""
        st.session_state.user_last_name = ""
        st.session_state.user_phone_number = ""
        st.rerun()

if st.session_state.user_logged_in:
    st.title("📱 iPhone Order System")
    
    # Load menu
    menu = load_menu()
    
    # Create tabs for different sections
    tab_new, tab_orders, tab_update, tab_delete = st.tabs(["Place New Order", "View Orders", "Update Order", "Delete Order"])
    
    # ======================== TAB 1: PLACE NEW ORDER ========================
    with tab_new:
        st.subheader("Create New Order")
        
        with st.form("new_order_form"):
            st.write("**Shipping Information**")
            col1, col2 = st.columns(2)
            with col1:
                order_first_name = st.text_input("First Name", st.session_state.user_first_name)
            with col2:
                order_last_name = st.text_input("Last Name", st.session_state.user_last_name)
            
            order_phone_num = st.text_input("Phone Number", st.session_state.user_phone_number)
            order_address = st.text_input("Shipping Address")
            
            st.write("**iPhone Configuration**")
            col1, col2 = st.columns(2)
            with col1:
                order_model = st.selectbox("iPhone Model", menu.get("MODEL", []))
            with col2:
                order_storage = st.selectbox("Storage", menu.get("STORAGE", []))
            
            order_color = st.selectbox("Color", menu.get("COLOR", []))
            
            st.write("**Add-ons**")
            col1, col2 = st.columns(2)
            with col1:
                order_applecare = st.selectbox("AppleCare+", menu.get("APPLECARE", []))
            with col2:
                order_charger = st.selectbox("Fast Charger", menu.get("CHARGER", []))
            
            # Calculate and display total
            order_total = calculate_total(order_model, order_storage, order_applecare, order_charger)
            st.metric("Total Price", f"${order_total:.2f}")
            
            submit = st.form_submit_button("Place Order")
            
            if submit:
                # Validation
                if not order_first_name or not order_last_name or not order_phone_num or not order_address:
                    st.error("Please fill in all customer information fields")
                else:
                    save_order(
                        order_first_name.title(),
                        order_last_name.title(),
                        order_phone_num,
                        order_address,
                        order_model,
                        order_storage,
                        order_color,
                        order_applecare,
                        order_charger,
                        order_total
                    )
                    st.success("Order placed successfully!")
                    st.balloons()
    
    # ======================== TAB 2: VIEW ORDERS ========================
    with tab_orders:
        st.subheader("5 Most Recent Orders")
        
        recent = get_recent_orders(5)
        
        if not recent:
            st.info("No orders found yet")
        else:
            for idx, order in enumerate(recent):
                with st.expander(f"Order {idx + 1} - {order['timestamp']} | {order['first_name']} {order['last_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Customer:** {order['first_name']} {order['last_name']}")
                        st.write(f"**Phone:** {order['phone_number']}")
                        st.write(f"**Address:** {order['address']}")
                    with col2:
                        st.write(f"**Model:** {order['model']}")
                        st.write(f"**Storage:** {order['storage']}")
                        st.write(f"**Color:** {order['color']}")
                    
                    st.write(f"**AppleCare+:** {order['applecare']}")
                    st.write(f"**Fast Charger:** {order['charger']}")
                    st.metric("Total", f"${order['total']:.2f}")
    
    # ======================== TAB 3: UPDATE ORDER ========================
    with tab_update:
        st.subheader("Update Most Recent Order")
        
        recent = get_recent_orders(1)
        
        if not recent:
            st.info("No orders to update")
        else:
            order = recent[0]
            st.write(f"**Updating:** {order['first_name']} {order['last_name']} - {order['timestamp']}")
            
            with st.form("update_order_form"):
                col1, col2 = st.columns(2)
                with col1:
                    update_model = st.selectbox("iPhone Model", menu.get("MODEL", []), index=menu.get("MODEL", []).index(order['model']) if order['model'] in menu.get("MODEL", []) else 0)
                with col2:
                    update_storage = st.selectbox("Storage", menu.get("STORAGE", []), index=menu.get("STORAGE", []).index(order['storage']) if order['storage'] in menu.get("STORAGE", []) else 0)
                
                update_color = st.selectbox("Color", menu.get("COLOR", []), index=menu.get("COLOR", []).index(order['color']) if order['color'] in menu.get("COLOR", []) else 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    update_applecare = st.selectbox("AppleCare+", menu.get("APPLECARE", []), index=menu.get("APPLECARE", []).index(order['applecare']) if order['applecare'] in menu.get("APPLECARE", []) else 0)
                with col2:
                    update_charger = st.selectbox("Fast Charger", menu.get("CHARGER", []), index=menu.get("CHARGER", []).index(order['charger']) if order['charger'] in menu.get("CHARGER", []) else 0)
                
                update_total = calculate_total(update_model, update_storage, update_applecare, update_charger)
                st.metric("New Total", f"${update_total:.2f}")
                
                update_submit = st.form_submit_button("Update Order")
                
                if update_submit:
                    update_order(0, update_model, update_storage, update_color, update_applecare, update_charger)
    
    # ======================== TAB 4: DELETE ORDER ========================
    with tab_delete:
        st.subheader("Delete Most Recent Order")
        
        recent = get_recent_orders(1)
        
        if not recent:
            st.info("No orders to delete")
        else:
            order = recent[0]
            st.warning(f"⚠️ Are you sure you want to delete this order?")
            st.write(f"**Customer:** {order['first_name']} {order['last_name']}")
            st.write(f"**Model:** {order['model']} - {order['storage']} - {order['color']}")
            st.write(f"**Total:** ${order['total']:.2f}")
            st.write(f"**Timestamp:** {order['timestamp']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Delete", type="secondary"):
                    delete_order(0)
                    st.rerun()
            with col2:
                st.write("Or go back to cancel")

else:
    st.title("📱 iPhone Order System")
    st.info("Please login or create an account to get started!")

