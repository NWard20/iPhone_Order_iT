# Session Memory: iPhone Order System Project

**Last Updated:** April 28, 2026  
**Status:** Streamlit app completed and tested

---

## Project Overview
- **Owner:** NWard20 (paired programming student)
- **Project:** Convert CLI-based iPhone ordering system to web app using Streamlit
- **Completion:** Fully functional - all 4 tabs working

---

## Current System Architecture

### Files Structure
```
/Copy_iPhone_Order_iT/
├── iphone_order.py          # IPhoneOrder class (REFACTORED)
├── IPhone_Online_System.py  # CLI helper functions (REFACTORED)
├── menu.txt                 # Format: "KEY ; option1, option2, ..."
├── order_history.txt        # Format: timestamp|first|last|phone|address|model|storage|color|applecare|charger|total
├── latest_receipt.txt       # Generated receipt file
└── ...

/streamlit_app.py            # NEW - Main Streamlit web app
```

### Data Format (IMPORTANT)
Order storage uses **pipe-delimited format with 11 fields**:
```
2026-04-28 02:52:08|John|Doe|(555) 123-4567|123 Main St, Springfield, IL 62701|Standard|128GB|Black|Yes|Yes|1027.00
```

Fields in order: timestamp|first_name|last_name|phone_number|address|model|storage|color|applecare|charger|total

### Pricing Structure (Hardcoded in streamlit_app.py)
- **Models:** Standard ($799), Plus ($899), Pro ($999), Pro Max ($1199)
- **Storage:** 128GB (+$0), 256GB (+$100), 512GB (+$300), 1TB (+$500)
- **Add-ons:** AppleCare+ (+$199), Fast Charger (+$29)

---

## Key Design Decisions Made

### 1. Refactored IPhoneOrder Class
- **Changed from:** `__init__(self, customer, address)`
- **Changed to:** `__init__(self, first_name, last_name, phone_number, address)`
- **Reason:** Better data separation, matches form fields
- **Status:** Works for both CLI and Streamlit

### 2. Sidebar-Based Login (Streamlit)
- Uses session_state to maintain login across reruns
- Two tabs: Login and Create Account
- No database - just session memory (no persistence between sessions)
- Shows user info: "Logged in as: FirstName LastName, Phone: XXX"

### 3. Tab-Based Navigation
- **Tab 1: Place New Order** - Form with all options, real-time price calc
- **Tab 2: View Orders** - Shows 5 most recent orders in expanders
- **Tab 3: Update Order** - Edit the most recent order only
- **Tab 4: Delete Order** - Delete the most recent order with confirmation

### 4. File-Based Data Storage
- Orders appended to `order_history.txt`
- Latest receipt written to `latest_receipt.txt` (overwrites each time)
- No database - works for learning project
- **Limitation:** Mixed old/new format in order_history.txt (old entries are comma-separated)

---

## Important Variables & Constants

### streamlit_app.py Session State Keys
- `user_logged_in` (bool)
- `user_first_name` (str)
- `user_last_name` (str)
- `user_phone_number` (str)

### File Paths (All Relative)
- `DATA_FILE = "Copy_iPhone_Order_iT/order_history.txt"`
- `MENU_FILE = "Copy_iPhone_Order_iT/menu.txt"`
- `HUMAN_REPORT = "Copy_iPhone_Order_iT/latest_receipt.txt"`

### Menu Options (From menu.txt)
- MODEL: Standard, Plus, Pro, Pro Max
- STORAGE: 128GB, 256GB, 512GB, 1TB
- COLOR: Black, Silver, Blue, Gold, Purple
- APPLECARE: Yes, No
- CHARGER: Yes, No

---

## What Works Well ✅
1. Full order creation flow with validation
2. Real-time total price calculation
3. Viewing last 5 orders with expandable details
4. Updating/deleting most recent order
5. Session state persists during app interaction
6. Menu options load from menu.txt dynamically
7. Proper form submission with st.form()

---

## Known Limitations/Issues

1. **Data Format Migration**
   - Old orders in file use different format (comma-separated)
   - New orders use pipe-delimited (11 fields)
   - Mixing works because we only parse new format, but file looks inconsistent

2. **Update/Delete Operations**
   - Only work on MOST RECENT order
   - Not user-specific (all users see all orders)
   - Updates require rewriting entire file

3. **No User Persistence**
   - Login info only stored in session
   - Closes when browser closed or app reloads
   - No user accounts/authentication

4. **No Input Sanitization**
   - Phone number/address accepted as-is
   - No validation for special characters or phone format
   - Works for educational project but would need hardening for production

---

## For Next Session - Questions to Ask

1. **Data Cleanup:** Should we migrate old orders to new format?
2. **Features:** Any new requirements or changes?
3. **Deployment:** Ready to deploy? Where?
4. **Testing:** Want to add automated tests?
5. **Scaling:** More than 100 orders? Should we use a database?

---

## Tips for Continued Development

- Always check both `iphone_order.py` (class) AND `streamlit_app.py` when making changes
- Menu changes should go in `menu.txt`, not hardcoded
- Remember the 11-field pipe-delimited format when reading orders
- Session state resets on every Streamlit interaction (by design)
- Use `st.rerun()` when you need to refresh the UI after state changes

---

## Commands to Run App
```bash
cd /workspaces/iPhone_Order_iT
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

---

## Git Status
- User configured with: `NWard20` / `nickward212@icloud.com`
- Current branch: main
- No commits made yet in this session (remember to commit!)

