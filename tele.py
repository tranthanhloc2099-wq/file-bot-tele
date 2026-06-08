import telebot
import time
import os
import threading
import requests
import random
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8910856673:AAH0al_odzz6O4bxrWdNLlCDDGOAB9wkKsI"
URL_CHUI = "https://raw.githubusercontent.com/tranthanhloc2099-wq/file-bot/refs/heads/main/chui.txt"

bot = telebot.TeleBot(TOKEN)
ADMIN_IDS = [8266903635]

# ============ BIẾN TOÀN CỤC ============
dang_chay = {"sp": False, "sp2": False, "spnd": False, "spstick": False}
event_dung = {"sp": threading.Event(), "sp2": threading.Event(), "spnd": threading.Event(), "spstick": threading.Event()}

TOC_DO_SPAM = 0.5
CHE_DO_SLOW = False
THOI_GIAN_SLOW = 1.0

CAU_CHUI_DOC_QUYEN = "BỌN ANH CHUYÊN DUYỆT BỌN ĐÚ MXH⚜️🔱ㅤㅤㅤ🌪️ ° 🦈 • .°• 🦎 ㅤ✯ ㅤ★ㅤ * ㅤ ° ㅤ 🦖🌟ㅤㅤㅤ🌏 ° 🔱 • .°• ✨ ㅤ✯ ㅤ★ㅤ * VÀ LÀ CƠN ÁC MỌNG KHI NGHE ĐẾN BỌN ANH⚜️🐲ㅤㅤㅤ🌏 ° 🦈 • .°• 🚀 ㅤ✯ ㅤ★ㅤ * ㅤ ° ㅤ ⚡🌟ㅤㅤㅤ🌏 ° 🌪️ • .°• 🚀 ㅤ✯ ㅤ★ㅤ * 𝐍𝐄̂𝐍 𝐀𝐍𝐇 𝐓𝐇𝐈́𝐂𝐇 𝐒𝐈̉ 𝐍𝐇𝐔̣𝐂 𝐋𝐔̃ Đ𝐔́ 𝐍𝐇𝐔̛ 𝐁𝐎̣𝐍 𝐌𝐀̀𝐘 🚀🎠🧸👾🦈 ° 🐲 ⚜️ ☄️ ° 🔱 • .°• 🚀 ✯ ★ * ° 🛰 °· ⚜️ 🌎🇻🇳🇻🇳🇻🇳"

users_data = {}
daily_lixi = {}
daily_kiemxu = {}
user_bet_amounts = {}

# ============ BIẾN VÉ SỐ ============
ve_so_data = {}
ket_qua_xo_so = None
thoi_gian_mo_thuong = None
lich_su_trung_thuong = []

# ============ BIẾN LỘC ============
loc_data = {}

# ============ HÀM HỖ TRỢ ============
def tai_noi_dung_chui():
    try:
        r = requests.get(URL_CHUI, timeout=10)
        if r.status_code == 200:
            return [line.strip() for line in r.text.splitlines() if line.strip()]
    except:
        pass
    return ["🔴 Spam test 1", "🟠 Spam test 2", "🟡 Spam test 3"]

def lay_thoi_gian_cho():
    if CHE_DO_SLOW:
        return TOC_DO_SPAM + THOI_GIAN_SLOW
    return TOC_DO_SPAM

def sleep_co_the_ngat(giay, loai):
    for _ in range(int(giay * 10)):
        if event_dung[loai].is_set():
            return False
        time.sleep(0.1)
    return True

def khoi_tao_user(user_id):
    if user_id not in users_data:
        users_data[user_id] = {"tien": 100000, "thang": 0, "thua": 0}

def get_hidden_mention(user_input):
    """Tạo hidden mention từ ID hoặc username"""
    if not user_input:
        return None, None
    
    user_input = user_input.strip()
    
    if user_input.isdigit():
        user_id = int(user_input)
        return user_id, f'<a href="tg://user?id={user_id}">&#8203;</a>'
    
    if user_input.startswith('@'):
        try:
            user_info = bot.get_chat(user_input)
            user_id = user_info.id
            return user_id, f'<a href="tg://user?id={user_id}">&#8203;</a>'
        except:
            return None, None
    
    return None, None

# ============ MENU CHÍNH ============
def menu_chinh():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("⚔️ SPAM", callback_data="open_spam_menu"),
        InlineKeyboardButton("🎮 GAME", callback_data="open_game_menu")
    ]
    markup.add(*buttons)
    return markup

def menu_spam_chinh():
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("🔙 QUAY LẠI MENU CHÍNH", callback_data="back_to_main")
    ]
    for btn in buttons:
        markup.add(btn)
    return markup

def menu_game_chinh():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🎲 Tài Xỉu", callback_data="menu_roll"),
        InlineKeyboardButton("🎃 Bầu Cua", callback_data="menu_baucua"),
        InlineKeyboardButton("🎫 Mua Vé Số", callback_data="menu_ve_so"),
        InlineKeyboardButton("💰 Xem Tiền", callback_data="xem_tien"),
        InlineKeyboardButton("📊 Top Xu", callback_data="menu_topxu"),
        InlineKeyboardButton("💼 Kiếm Xu", callback_data="help_kiemxu"),
        InlineKeyboardButton("🧧 Lì Xì", callback_data="help_lixi"),
        InlineKeyboardButton("🤝 Tặng Xu", callback_data="help_tangxu"),
        InlineKeyboardButton("🌊 Rải Lộc", callback_data="help_loc"),
        InlineKeyboardButton("📋 Xem Lộc", callback_data="help_xemloc"),
        InlineKeyboardButton("🔙 QUAY LẠI MENU CHÍNH", callback_data="back_to_main")
    ]
    for btn in buttons:
        markup.add(btn)
    return markup

def menu_admin_chinh():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("⚔️ SPAM", callback_data="open_spam_menu"),
        InlineKeyboardButton("🎮 GAME", callback_data="open_game_menu"),
        InlineKeyboardButton("👑 ADMIN PANEL", callback_data="admin_panel"),
        InlineKeyboardButton("🔙 QUAY LẠI", callback_data="back_to_main")
    ]
    markup.add(*buttons)
    return markup

def menu_admin_settings():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🧧 LÌ XÌ ADMIN", callback_data="admin_lixi"),
        InlineKeyboardButton("📊 THỐNG KÊ USER", callback_data="admin_stats"),
        InlineKeyboardButton("⚙️ SET SPEED", callback_data="admin_speed"),
        InlineKeyboardButton("🐢 SLOW MODE", callback_data="admin_slow"),
        InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
        InlineKeyboardButton("🔙 QUAY LẠI MENU ADMIN", callback_data="back_to_admin_main")
    )
    return markup

def menu_admin_lixi():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🎁 LÌ XÌ 10K", callback_data="lixi_admin_10000"),
        InlineKeyboardButton("🎁 LÌ XÌ 50K", callback_data="lixi_admin_50000"),
        InlineKeyboardButton("🎁 LÌ XÌ 100K", callback_data="lixi_admin_100000"),
        InlineKeyboardButton("🎁 LÌ XÌ 500K", callback_data="lixi_admin_500000"),
        InlineKeyboardButton("🎁 LÌ XÌ 1TR", callback_data="lixi_admin_1000000"),
        InlineKeyboardButton("🎁 LÌ XÌ 5TR", callback_data="lixi_admin_5000000"),
        InlineKeyboardButton("🎁 LÌ XÌ 10TR", callback_data="lixi_admin_10000000"),
        InlineKeyboardButton("✏️ NHẬP SỐ TIỀN", callback_data="lixi_admin_manual"),
        InlineKeyboardButton("🔙 QUAY LẠI", callback_data="admin_panel")
    ]
    for btn in buttons:
        markup.add(btn)
    return markup

def menu_roll():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎲 TÀI (11-18)", callback_data="bet_tai"),
        InlineKeyboardButton("🎰 XỈU (3-10)", callback_data="bet_xiu")
    )
    markup.add(InlineKeyboardButton("🔙 QUAY LẠI MENU GAME", callback_data="back_to_game_menu"))
    return markup

def menu_baucua():
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton("🐟", callback_data="bau_ca"),
        InlineKeyboardButton("🦐", callback_data="bau_tom"),
        InlineKeyboardButton("🦀", callback_data="bau_cua"),
        InlineKeyboardButton("🐓", callback_data="bau_ga"),
        InlineKeyboardButton("🌿", callback_data="bau_ngusac"),
        InlineKeyboardButton("🐯", callback_data="bau_ho")
    ]
    for btn in buttons:
        markup.add(btn)
    markup.add(InlineKeyboardButton("💰 ĐỔI TIỀN CƯỢC", callback_data="bau_change_bet"))
    markup.add(InlineKeyboardButton("🔙 QUAY LẠI MENU GAME", callback_data="back_to_game_menu"))
    return markup

def menu_baucua_cuoc():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("💰 1K", callback_data="bau_set_1000"),
        InlineKeyboardButton("💰 5K", callback_data="bau_set_5000"),
        InlineKeyboardButton("💰 10K", callback_data="bau_set_10000"),
        InlineKeyboardButton("💰 50K", callback_data="bau_set_50000"),
        InlineKeyboardButton("💰 100K", callback_data="bau_set_100000"),
        InlineKeyboardButton("💰 500K", callback_data="bau_set_500000"),
        InlineKeyboardButton("🔙 QUAY LẠI", callback_data="menu_baucua")
    ]
    markup.add(*buttons)
    return markup

def menu_topxu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🔙 QUAY LẠI MENU GAME", callback_data="back_to_game_menu"))
    return markup

def menu_ve_so():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🎫 MUA VÉ SỐ (10K)", callback_data="ve_so_mua"),
        InlineKeyboardButton("📋 TRA CỨU VÉ", callback_data="ve_so_tra_cuu"),
        InlineKeyboardButton("🏆 KẾT QUẢ MỚI NHẤT", callback_data="ve_so_ket_qua"),
        InlineKeyboardButton("📊 LỊCH SỬ TRÚNG", callback_data="ve_so_lich_su"),
        InlineKeyboardButton("🎲 TỰ CHỌN SỐ", callback_data="ve_so_tu_chon"),
        InlineKeyboardButton("💰 MUA NHIỀU VÉ", callback_data="ve_so_mua_nhieu"),
        InlineKeyboardButton("🔙 QUAY LẠI MENU GAME", callback_data="back_to_game_menu")
    ]
    for btn in buttons:
        markup.add(btn)
    return markup

def menu_chon_so():
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(0, 10):
        buttons.append(InlineKeyboardButton(str(i), callback_data=f"chon_so_{i}"))
    for btn in buttons:
        markup.add(btn)
    markup.add(InlineKeyboardButton("✅ XÁC NHẬN", callback_data="chon_so_xac_nhan"))
    markup.add(InlineKeyboardButton("🔙 QUAY LẠI", callback_data="menu_ve_so"))
    return markup

def menu_nhan_loc(chat_id, so_tien_con_lai):
    markup = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(f"💰 NHẬN NGAY - {so_tien_con_lai:,}đ", callback_data=f"nhan_loc_{chat_id}")
    markup.add(btn)
    return markup

def menu_dat_cuoc_tuychinh(user_id, loai):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("100", callback_data=f"{loai}_100_{user_id}"),
        InlineKeyboardButton("500", callback_data=f"{loai}_500_{user_id}"),
        InlineKeyboardButton("1000", callback_data=f"{loai}_1000_{user_id}"),
        InlineKeyboardButton("5000", callback_data=f"{loai}_5000_{user_id}"),
        InlineKeyboardButton("10000", callback_data=f"{loai}_10000_{user_id}"),
        InlineKeyboardButton("50000", callback_data=f"{loai}_50000_{user_id}"),
        InlineKeyboardButton("100000", callback_data=f"{loai}_100000_{user_id}"),
        InlineKeyboardButton("🔙 HỦY", callback_data="menu_roll")
    ]
    for btn in buttons:
        markup.add(btn)
    markup.add(InlineKeyboardButton("✏️ NHẬP SỐ TIỀN", callback_data=f"manual_bet_{loai}_{user_id}"))
    return markup

# ============ HÀM XỬ LÝ SPAM ============
@bot.message_handler(commands=['sp'])
def spam(m):
    if dang_chay["sp"]:
        event_dung["sp"].set()
        time.sleep(0.1)
    event_dung["sp"].clear()
    threading.Thread(target=spam_thread, args=(m,), daemon=True).start()

def spam_thread(m):
    dang_chay["sp"] = True
    chat_id = m.chat.id
    cac_cau = tai_noi_dung_chui()
    parts = m.text.split()
    
    target_raw = parts[1] if len(parts) > 1 else ""
    
    hidden_mention = ""
    if target_raw:
        user_id, mention = get_hidden_mention(target_raw)
        if mention:
            hidden_mention = mention + " "
    
    delay = lay_thoi_gian_cho()
    bot.send_message(chat_id, f"🔥 BẮT ĐẦU SPAM | Delay: {delay}s | Target: {target_raw}", parse_mode="HTML")
    
    while dang_chay["sp"] and not event_dung["sp"].is_set():
        for cau in cac_cau:
            if not dang_chay["sp"] or event_dung["sp"].is_set():
                break
            msg = f"{hidden_mention}{cau}"
            bot.send_message(chat_id, msg, parse_mode="HTML")
            if not sleep_co_the_ngat(delay, "sp"):
                break
    bot.send_message(chat_id, "⚠️ Đã dừng spam!")

@bot.message_handler(commands=['sp2'])
def spam2(m):
    if dang_chay["sp2"]:
        event_dung["sp2"].set()
        time.sleep(0.1)
    event_dung["sp2"].clear()
    threading.Thread(target=spam2_thread, args=(m,), daemon=True).start()

def spam2_thread(m):
    dang_chay["sp2"] = True
    chat_id = m.chat.id
    parts = m.text.split()
    
    target_raw = parts[1] if len(parts) > 1 else ""
    
    hidden_mention = ""
    if target_raw:
        user_id, mention = get_hidden_mention(target_raw)
        if mention:
            hidden_mention = mention
    
    delay = lay_thoi_gian_cho()
    bot.send_message(chat_id, f"💀 BẮT ĐẦU SP2 | Delay: {delay}s | Target: {target_raw}", parse_mode="HTML")
    
    while dang_chay["sp2"] and not event_dung["sp2"].is_set():
        msg = f"{hidden_mention}{CAU_CHUI_DOC_QUYEN}"
        bot.send_message(chat_id, msg, parse_mode="HTML")
        if not sleep_co_the_ngat(delay, "sp2"):
            break
    bot.send_message(chat_id, "⚠️ Đã dừng sp2!")

@bot.message_handler(commands=['spnd'])
def spamnd(m):
    if dang_chay["spnd"]:
        event_dung["spnd"].set()
        time.sleep(0.1)
    event_dung["spnd"].clear()
    threading.Thread(target=spamnd_thread, args=(m,), daemon=True).start()

def spamnd_thread(m):
    dang_chay["spnd"] = True
    chat_id = m.chat.id
    parts = m.text.split()
    
    if len(parts) < 2:
        bot.send_message(chat_id, "⚠️ /spnd @user hoặc ID nội dung")
        dang_chay["spnd"] = False
        return
    
    hidden_mention = ""
    content = ""
    target_raw = ""
    
    first = parts[1]
    if first.startswith('@') or first.isdigit():
        target_raw = first
        user_id, mention = get_hidden_mention(target_raw)
        if mention:
            hidden_mention = mention + " "
        content = " ".join(parts[2:]) if len(parts) > 2 else ""
    else:
        content = " ".join(parts[1:])
    
    if not content:
        bot.send_message(chat_id, "⚠️ Thiếu nội dung spam!")
        dang_chay["spnd"] = False
        return
    
    delay = lay_thoi_gian_cho()
    bot.send_message(chat_id, f"📝 BẮT ĐẦU SPAM ND | Delay: {delay}s | Target: {target_raw if target_raw else 'Không'}")
    
    while dang_chay["spnd"] and not event_dung["spnd"].is_set():
        msg = f"{hidden_mention}{content}"
        bot.send_message(chat_id, msg, parse_mode="HTML")
        if not sleep_co_the_ngat(delay, "spnd"):
            break
    bot.send_message(chat_id, "⚠️ Đã dừng spam nd!")

@bot.message_handler(commands=['spstick'])
def spstick(m):
    if not m.reply_to_message or not m.reply_to_message.sticker:
        bot.reply_to(m, "⚠️ Reply vào sticker cần spam!\nCách dùng: reply sticker + /spstick @user hoặc ID")
        return
    
    if dang_chay["spstick"]:
        event_dung["spstick"].set()
        time.sleep(0.1)
    event_dung["spstick"].clear()
    threading.Thread(target=spstick_thread, args=(m,), daemon=True).start()

def spstick_thread(m):
    dang_chay["spstick"] = True
    chat_id = m.chat.id
    sticker_id = m.reply_to_message.sticker.file_id
    delay = lay_thoi_gian_cho()
    
    parts = m.text.split()
    target_raw = parts[1] if len(parts) > 1 else ""
    
    hidden_mention = ""
    if target_raw:
        user_id, mention = get_hidden_mention(target_raw)
        if mention:
            hidden_mention = mention
    
    bot.send_message(chat_id, f"🎨 BẮT ĐẦU SPAM STICKER | Delay: {delay}s | Target: {target_raw if target_raw else 'Không'}", parse_mode="HTML")
    
    while dang_chay["spstick"] and not event_dung["spstick"].is_set():
        try:
            if hidden_mention:
                bot.send_message(chat_id, hidden_mention, parse_mode="HTML", disable_notification=True)
                time.sleep(0.3)
            bot.send_sticker(chat_id, sticker_id)
        except:
            break
        if not sleep_co_the_ngat(delay, "spstick"):
            break
    bot.send_message(chat_id, "⚠️ Đã dừng spam sticker!")

@bot.message_handler(commands=['stop'])
def stop_all(m):
    for key in dang_chay:
        dang_chay[key] = False
        event_dung[key].set()
    time.sleep(0.1)
    for key in event_dung:
        event_dung[key].clear()
    bot.reply_to(m, "🛑 **ĐÃ DỪNG HẾT SPAM!**")

@bot.message_handler(commands=['clearall'])
def clear_all(m):
    chat_id = m.chat.id
    msg_id = m.message_id
    deleted = 0
    for i in range(200):
        try:
            bot.delete_message(chat_id, msg_id - i)
            deleted += 1
        except:
            continue
    bot.reply_to(m, f"🗑️ Đã xóa {deleted} tin nhắn")

# ============ GAME TÀI XỈU ============
@bot.callback_query_handler(func=lambda call: call.data == "menu_roll")
def show_roll_menu(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    bot.edit_message_text(
        f"🎲 **TÀI XỈU CASINO** 🎲\n━━━━━━━━━━━━━━━━━━━━\n💰 Số tiền: {users_data[user_id]['tien']:,}đ\n\n⚀ ⚁ ⚂ ⚃ ⚄ ⚅\n\n🔴 **TÀI** - Tổng 11 đến 18 (x2 tiền)\n⚫ **XỈU** - Tổng 3 đến 10 (x2 tiền)\n\n👉 Chọn cửa để bắt đầu:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_roll(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["bet_tai", "bet_xiu"])
def handle_bet(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    if users_data[user_id]["tien"] < 100:
        bot.answer_callback_query(call.id, "❌ Bạn không đủ 100đ để chơi!", show_alert=True)
        return
    loai = "tai" if call.data == "bet_tai" else "xiu"
    bot.edit_message_text(
        f"🎲 **CỬA {loai.upper()}** 🎲\n━━━━━━━━━━━━━━━━━━━━\n💰 Số tiền hiện có: {users_data[user_id]['tien']:,}đ\n\n👇 Chọn số tiền cược:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_dat_cuoc_tuychinh(user_id, loai), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("tai_") or call.data.startswith("xiu_"))
def xu_ly_tai_xiu(call):
    parts = call.data.split("_")
    loai = parts[0]
    so_tien = int(parts[1])
    user_id_cuoc = int(parts[2])
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if user_id != user_id_cuoc:
        bot.answer_callback_query(call.id, "❌ Không phải phiên của bạn!", show_alert=True)
        return
    
    khoi_tao_user(user_id)
    if users_data[user_id]["tien"] < so_tien:
        bot.answer_callback_query(call.id, f"❌ Bạn không đủ {so_tien:,}đ để cược!", show_alert=True)
        return
    
    users_data[user_id]["tien"] -= so_tien
    bot.delete_message(chat_id, msg_id)
    
    msg1 = bot.send_dice(chat_id, emoji="🎲")
    time.sleep(0.8)
    msg2 = bot.send_dice(chat_id, emoji="🎲")
    time.sleep(1.3)
    msg3 = bot.send_dice(chat_id, emoji="🎲")
    time.sleep(1.8)
    
    dice1, dice2, dice3 = msg1.dice.value, msg2.dice.value, msg3.dice.value
    tong = dice1 + dice2 + dice3
    ket_qua = "tai" if tong >= 11 else "xiu"
    icon_map = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    
    if ket_qua == loai:
        thuong = so_tien * 2
        users_data[user_id]["tien"] += thuong
        users_data[user_id]["thang"] += 1
        bot.send_message(chat_id, f"🎉 **KẾT QUẢ TÀI XỈU** 🎉\n━━━━━━━━━━━━━━━━━━━━\n🎲 {icon_map[dice1]} {icon_map[dice2]} {icon_map[dice3]}\n🔢 **Tổng:** {tong}\n✅ **BẠN THẮNG!**\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền cược:** -{so_tien:,}đ\n💎 **Tiền thắng:** +{thuong:,}đ\n📊 **Lãi:** +{thuong - so_tien:,}đ\n💎 **Số dư mới:** {users_data[user_id]['tien']:,}đ", parse_mode="Markdown")
    else:
        users_data[user_id]["thua"] += 1
        bot.send_message(chat_id, f"💀 **KẾT QUẢ TÀI XỈU** 💀\n━━━━━━━━━━━━━━━━━━━━\n🎲 {icon_map[dice1]} {icon_map[dice2]} {icon_map[dice3]}\n🔢 **Tổng:** {tong}\n❌ **BẠN THUA!**\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền cược:** -{so_tien:,}đ\n💎 **Tiền thắng:** +0đ\n📊 **Lỗ:** -{so_tien:,}đ\n💎 **Số dư mới:** {users_data[user_id]['tien']:,}đ", parse_mode="Markdown")
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎲 CHƠI LẠI", callback_data="menu_roll"), InlineKeyboardButton("🔙 MENU GAME", callback_data="back_to_game_menu"))
    bot.send_message(chat_id, "👇 **Chọn tiếp:**", reply_markup=markup)

# ============ GAME BẦU CUA - RANDOM 3 LINH VẬT ============
linh_vat_icons = {"🐟": "CÁ", "🦐": "TÔM", "🦀": "CUA", "🐓": "GÀ", "🌿": "NGŨ SẮC", "🐯": "HỔ"}

STICKER_LINH_VAT = {
    "🐟": "CAACAgQAAxkBAAEBAg",
    "🦐": "CAACAgQAAxkBAAEBAh",
    "🦀": "CAACAgQAAxkBAAEBAi",
    "🐓": "CAACAgQAAxkBAAEBAj",
    "🌿": "CAACAgQAAxkBAAEBAk",
    "🐯": "CAACAgQAAxkBAAEBAl"
}

@bot.callback_query_handler(func=lambda call: call.data == "menu_baucua")
def show_baucua_menu(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    cuoc_mac_dinh = user_bet_amounts.get(user_id, {}).get("baucua", 1000)
    bot.edit_message_text(
        f"🎃 **BẦU CUA TÔM CÁ** 🎃\n━━━━━━━━━━━━━━━━━━━━\n💰 **Số tiền:** {users_data[user_id]['tien']:,}đ\n💸 **Tiền cược:** {cuoc_mac_dinh:,}đ\n━━━━━━━━━━━━━━━━━━━━\n🐟  🦐  🦀  🐓  🌿  🐯\n━━━━━━━━━━━━━━━━━━━━\n👉 **Chọn linh vật để đặt cược:**",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_baucua(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["bau_ca", "bau_tom", "bau_cua", "bau_ga", "bau_ngusac", "bau_ho"])
def handle_baucua(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    icon_map = {"bau_ca": "🐟", "bau_tom": "🦐", "bau_cua": "🦀", "bau_ga": "🐓", "bau_ngusac": "🌿", "bau_ho": "🐯"}
    linh_vat_chon_icon = icon_map[call.data]
    linh_vat_chon_ten = linh_vat_icons[linh_vat_chon_icon]
    cuoc = user_bet_amounts.get(user_id, {}).get("baucua", 1000)
    
    khoi_tao_user(user_id)
    if users_data[user_id]["tien"] < cuoc:
        bot.answer_callback_query(call.id, f"❌ Bạn không đủ {cuoc:,}đ để cược!", show_alert=True)
        return
    
    users_data[user_id]["tien"] -= cuoc
    bot.delete_message(chat_id, msg_id)
    
    danh_sach_linh_vat = list(linh_vat_icons.keys())
    ket_qua_3_linh_vat = [random.choice(danh_sach_linh_vat) for _ in range(3)]
    
    for linh_vat in ket_qua_3_linh_vat:
        sticker_id = STICKER_LINH_VAT.get(linh_vat)
        if sticker_id:
            bot.send_sticker(chat_id, sticker_id)
            time.sleep(0.8)
        else:
            bot.send_message(chat_id, f"🎲 {linh_vat}")
            time.sleep(0.5)
    
    time.sleep(1)
    
    so_lan_trung = ket_qua_3_linh_vat.count(linh_vat_chon_icon)
    
    if so_lan_trung > 0:
        thuong = cuoc * 2 * so_lan_trung
        users_data[user_id]["tien"] += thuong
        users_data[user_id]["thang"] += 1
        
        ket_qua_str = " + ".join([linh_vat_icons[v] for v in ket_qua_3_linh_vat])
        
        bot.send_message(chat_id, 
            f"🎉 **KẾT QUẢ BẦU CUA** 🎉\n━━━━━━━━━━━━━━━━━━━━\n🎰 **Kết quả:** {ket_qua_str}\n🎯 **Bạn cược:** {linh_vat_chon_icon} - {linh_vat_chon_ten}\n✅ **TRÙNG {so_lan_trung} LẦN!**\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền cược:** -{cuoc:,}đ\n💎 **Tiền thưởng:** +{thuong:,}đ\n📊 **Lãi:** +{thuong - cuoc:,}đ\n💎 **Số dư mới:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━\n🐟 🦐 🦀 🐓 🌿 🐯", 
            parse_mode="Markdown")
    else:
        users_data[user_id]["thua"] += 1
        
        ket_qua_str = " + ".join([linh_vat_icons[v] for v in ket_qua_3_linh_vat])
        
        bot.send_message(chat_id, 
            f"💀 **KẾT QUẢ BẦU CUA** 💀\n━━━━━━━━━━━━━━━━━━━━\n🎰 **Kết quả:** {ket_qua_str}\n🎯 **Bạn cược:** {linh_vat_chon_icon} - {linh_vat_chon_ten}\n❌ **KHÔNG TRÙNG!**\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền cược:** -{cuoc:,}đ\n💎 **Tiền thắng:** +0đ\n📊 **Lỗ:** -{cuoc:,}đ\n💎 **Số dư mới:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━\n🐟 🦐 🦀 🐓 🌿 🐯", 
            parse_mode="Markdown")
    
    time.sleep(0.5)
    bot.send_message(chat_id, "👇 **Chơi tiếp:**", reply_markup=menu_baucua())

@bot.callback_query_handler(func=lambda call: call.data == "bau_change_bet")
def handle_bau_change_bet(call):
    user_id = call.from_user.id
    bot.edit_message_text(
        f"🎃 **CHỌN TIỀN CƯỢC BẦU CUA** 🎃\n━━━━━━━━━━━━━━━━━━━━\n💰 **Số dư hiện tại:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━\n👇 **Chọn mức cược:**",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_baucua_cuoc(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("bau_set_"))
def handle_bau_set_cuoc(call):
    user_id = call.from_user.id
    so_tien = int(call.data.split("_")[2])
    if user_id not in user_bet_amounts:
        user_bet_amounts[user_id] = {}
    user_bet_amounts[user_id]["baucua"] = so_tien
    bot.answer_callback_query(call.id, f"✅ Đã đặt cược: {so_tien:,}đ", show_alert=True)
    bot.edit_message_text(
        f"🎃 **BẦU CUA TÔM CÁ** 🎃\n━━━━━━━━━━━━━━━━━━━━\n💰 **Số tiền:** {users_data[user_id]['tien']:,}đ\n💸 **Tiền cược:** {so_tien:,}đ\n━━━━━━━━━━━━━━━━━━━━\n🐟  🦐  🦀  🐓  🌿  🐯\n━━━━━━━━━━━━━━━━━━━━\n👉 **Chọn linh vật để đặt cược:**",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_baucua(), parse_mode="Markdown"
    )

# ============ GAME TOP XU ============
@bot.callback_query_handler(func=lambda call: call.data == "menu_topxu")
def show_topxu(call):
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]["tien"], reverse=True)[:10]
    msg = "📊 **TOP XU** 📊\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, (uid, data) in enumerate(sorted_users, 1):
        try:
            user = bot.get_chat(uid)
            name = user.first_name or str(uid)
        except:
            name = str(uid)
        msg += f"{i}. {name}: {data['tien']:,}đ\n"
    msg += "━━━━━━━━━━━━━━━━━━━━"
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=menu_topxu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "xem_tien")
def xem_tien(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    bot.answer_callback_query(call.id, f"Số dư: {users_data[user_id]['tien']:,}đ | Thắng: {users_data[user_id]['thang']} | Thua: {users_data[user_id]['thua']}", show_alert=True)

# ============ VÉ SỐ ============
def tinh_giai_thuong(ket_qua):
    if ket_qua[0] == ket_qua[1] == ket_qua[2]:
        return {"ten": "GIẢI ĐẶC BIỆT", "ti_le": 100}
    if ket_qua[1] == ket_qua[2]:
        return {"ten": "GIẢI NHẤT", "ti_le": 20}
    if ket_qua[0] == ket_qua[1]:
        return {"ten": "GIẢI NHÌ", "ti_le": 10}
    if ket_qua[0] == ket_qua[2]:
        return {"ten": "GIẢI BA", "ti_le": 5}
    return {"ten": "GIẢI KHUYẾN KHÍCH", "ti_le": 2}

def thong_bao_ket_qua(ket_qua):
    so_str = " ".join(map(str, ket_qua))
    giai_thuong = tinh_giai_thuong(ket_qua)
    msg = f"🎉 **KẾT QUẢ XỔ SỐ** 🎉\n━━━━━━━━━━━━━━━━━━━━\n🎯 **Kết quả:** {so_str}\n🏆 **Giải:** {giai_thuong['ten']}\n💰 **Tỉ lệ trả thưởng:** x{giai_thuong['ti_le']}\n━━━━━━━━━━━━━━━━━━━━"
    for user_id in ve_so_data:
        try:
            bot.send_message(user_id, msg, parse_mode="Markdown")
        except:
            pass

def trao_thuong(ket_qua):
    so_str = "".join(map(str, ket_qua))
    giai_thuong = tinh_giai_thuong(ket_qua)
    for user_id, data in ve_so_data.items():
        for ve in data["ve"]:
            if ve["so"] == so_str:
                tien_thuong = ve["so_tien"] * giai_thuong["ti_le"]
                khoi_tao_user(user_id)
                users_data[user_id]["tien"] += tien_thuong
                lich_su_trung_thuong.append({
                    "user_id": user_id,
                    "so": so_str,
                    "tien_thuong": tien_thuong,
                    "thoi_gian": datetime.now()
                })
                try:
                    bot.send_message(user_id, f"🎉🎉🎉 **CHÚC MỪNG BẠN TRÚNG THƯỞNG!** 🎉🎉🎉\n━━━━━━━━━━━━━━━━━━━━\n🎯 **Số trúng:** {so_str}\n🏆 **Giải:** {giai_thuong['ten']}\n💰 **Tiền thưởng:** +{tien_thuong:,}đ\n💎 **Số dư mới:** {users_data[user_id]['tien']:,}đ", parse_mode="Markdown")
                except:
                    pass
                ve_so_data[user_id]["ve"].remove(ve)
    for user_id in list(ve_so_data.keys()):
        ve_so_data[user_id]["ve"] = [v for v in ve_so_data[user_id]["ve"] if v["ky"] > 0]

def mua_ve_so(user_id, so_duoc_chon=None, so_luong=1):
    khoi_tao_user(user_id)
    gia_ve = 10000
    tong_tien = gia_ve * so_luong
    if users_data[user_id]["tien"] < tong_tien:
        return False, f"❌ Bạn không đủ {tong_tien:,}đ để mua {so_luong} vé!"
    users_data[user_id]["tien"] -= tong_tien
    if user_id not in ve_so_data:
        ve_so_data[user_id] = {"ve": []}
    for i in range(so_luong):
        if so_duoc_chon:
            so = so_duoc_chon
        else:
            so = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
        ve_so_data[user_id]["ve"].append({"so": so, "so_tien": gia_ve, "ngay_mua": datetime.now(), "ky": 1})
    return True, f"✅ Đã mua {so_luong} vé số với giá {tong_tien:,}đ!\n🎫 Số của bạn: {', '.join([v['so'] for v in ve_so_data[user_id]['ve'][-so_luong:]])}\n⏰ Mở thưởng sau 30 giây!"

def mo_thuong_tu_dong():
    global ket_qua_xo_so, thoi_gian_mo_thuong
    while True:
        if thoi_gian_mo_thuong and datetime.now() >= thoi_gian_mo_thuong:
            ket_qua = [random.randint(0, 9) for _ in range(3)]
            ket_qua_xo_so = {"so": ket_qua, "thoi_gian": datetime.now(), "giai_thuong": tinh_giai_thuong(ket_qua)}
            thong_bao_ket_qua(ket_qua)
            trao_thuong(ket_qua)
            thoi_gian_mo_thuong = datetime.now() + timedelta(seconds=30)
        time.sleep(1)

@bot.callback_query_handler(func=lambda call: call.data == "menu_ve_so")
def show_ve_so_menu(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    bot.edit_message_text(
        f"🎫 **MUA VÉ SỐ - VIETLOTT** 🎫\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🎯 Giá vé: 10,000đ/vé\n🏆 Giải thưởng:\n   • ĐB: x100\n   • Nhất: x20\n   • Nhì: x10\n   • Ba: x5\n   • KK: x2\n⏰ Mở thưởng sau 30 giây!\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_ve_so(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_mua")
def mua_ve_callback(call):
    user_id = call.from_user.id
    success, msg = mua_ve_so(user_id)
    bot.answer_callback_query(call.id, msg, show_alert=True)
    khoi_tao_user(user_id)
    bot.edit_message_text(
        f"🎫 **MUA VÉ SỐ - VIETLOTT** 🎫\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🎯 Giá vé: 10,000đ/vé\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_ve_so(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_tu_chon")
def tu_chon_so(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    if user_id not in ve_so_data:
        ve_so_data[user_id] = {"ve": [], "so_dang_chon": []}
    ve_so_data[user_id]["so_dang_chon"] = []
    bot.edit_message_text(
        f"🎲 **TỰ CHỌN SỐ MAY MẮN** 🎲\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n📝 Chọn 3 số (mỗi số từ 0-9)\n━━━━━━━━━━━━━━━━━━━━\n👇 Nhấn vào các số để chọn:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_chon_so(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("chon_so_"))
def chon_so_callback(call):
    user_id = call.from_user.id
    so = int(call.data.split("_")[2])
    if user_id not in ve_so_data:
        ve_so_data[user_id] = {"ve": [], "so_dang_chon": []}
    if len(ve_so_data[user_id]["so_dang_chon"]) < 3:
        ve_so_data[user_id]["so_dang_chon"].append(so)
        bot.answer_callback_query(call.id, f"✅ Đã chọn số {so}")
        so_da_chon = " ".join(map(str, ve_so_data[user_id]["so_dang_chon"]))
        bot.edit_message_text(
            f"🎲 **TỰ CHỌN SỐ MAY MẮN** 🎲\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n📝 Đã chọn: {so_da_chon}\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn tiếp hoặc nhấn XÁC NHẬN:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_chon_so(), parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "⚠️ Bạn đã chọn đủ 3 số! Nhấn XÁC NHẬN để mua vé!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "chon_so_xac_nhan")
def xac_nhan_chon_so(call):
    user_id = call.from_user.id
    if user_id not in ve_so_data or len(ve_so_data[user_id].get("so_dang_chon", [])) != 3:
        bot.answer_callback_query(call.id, "❌ Vui lòng chọn đủ 3 số!", show_alert=True)
        return
    so_chon = "".join(map(str, ve_so_data[user_id]["so_dang_chon"]))
    success, msg = mua_ve_so(user_id, so_chon)
    bot.answer_callback_query(call.id, msg, show_alert=True)
    ve_so_data[user_id]["so_dang_chon"] = []
    khoi_tao_user(user_id)
    bot.edit_message_text(
        f"🎫 **MUA VÉ SỐ - VIETLOTT** 🎫\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🎯 Giá vé: 10,000đ/vé\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_ve_so(), parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_tra_cuu")
def tra_cuu_ve(call):
    user_id = call.from_user.id
    if user_id not in ve_so_data or not ve_so_data[user_id]["ve"]:
        bot.answer_callback_query(call.id, "📭 Bạn chưa có vé số nào!", show_alert=True)
        return
    msg = "📋 **DANH SÁCH VÉ SỐ CỦA BẠN**\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, ve in enumerate(ve_so_data[user_id]["ve"], 1):
        msg += f"{i}. 🎫 Số: {ve['so']} - {ve['so_tien']:,}đ\n"
    msg += "━━━━━━━━━━━━━━━━━━━━\n⏰ Mở thưởng sau 30 giây!"
    bot.answer_callback_query(call.id, msg, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_ket_qua")
def xem_ket_qua(call):
    global ket_qua_xo_so
    if not ket_qua_xo_so:
        bot.answer_callback_query(call.id, "⏰ Chưa có kết quả nào! Hãy mua vé và chờ 30 giây!", show_alert=True)
        return
    so_str = " ".join(map(str, ket_qua_xo_so["so"]))
    giai = ket_qua_xo_so["giai_thuong"]
    thoi_gian = ket_qua_xo_so["thoi_gian"].strftime("%H:%M:%S")
    msg = f"🏆 **KẾT QUẢ XỔ SỐ MỚI NHẤT**\n━━━━━━━━━━━━━━━━━━━━\n🎯 Kết quả: {so_str}\n🏆 Giải: {giai['ten']}\n💰 Tỉ lệ: x{giai['ti_le']}\n⏰ Thời gian: {thoi_gian}\n━━━━━━━━━━━━━━━━━━━━"
    bot.answer_callback_query(call.id, msg, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_lich_su")
def lich_su_trung(call):
    if not lich_su_trung_thuong:
        bot.answer_callback_query(call.id, "📭 Chưa có ai trúng thưởng!", show_alert=True)
        return
    msg = "📊 **LỊCH SỬ TRÚNG THƯỞNG**\n━━━━━━━━━━━━━━━━━━━━\n"
    for item in lich_su_trung_thuong[-10:]:
        try:
            user = bot.get_chat(item["user_id"])
            name = user.first_name or str(item["user_id"])
        except:
            name = str(item["user_id"])
        msg += f"🎉 {name}: {item['so']} - +{item['tien_thuong']:,}đ\n"
    msg += "━━━━━━━━━━━━━━━━━━━━"
    bot.answer_callback_query(call.id, msg, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "ve_so_mua_nhieu")
def mua_nhieu_ve(call):
    msg = bot.send_message(call.message.chat.id, "💰 **NHẬP SỐ LƯỢNG VÉ MUỐN MUA**\n━━━━━━━━━━━━━━━━━━━━\n📝 Mỗi vé: 10,000đ\nVí dụ: `5` để mua 5 vé\n\n⚠️ Tối đa 10 vé/lần", parse_mode="Markdown")
    bot.register_next_step_handler(msg, xu_ly_mua_nhieu_ve, call.message)

def xu_ly_mua_nhieu_ve(message, original_msg):
    user_id = message.from_user.id
    try:
        so_luong = int(message.text.strip())
        if so_luong < 1 or so_luong > 10:
            bot.reply_to(message, "❌ Số lượng vé phải từ 1-10!")
            return
        success, msg = mua_ve_so(user_id, so_luong=so_luong)
        bot.reply_to(message, msg, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Vui lòng nhập số hợp lệ!")

# ============ RẢI LỘC - CHỈ 1 NGƯỜI NHẬN ============
@bot.message_handler(commands=['loc'])
def rai_loc(m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    parts = m.text.split()
    
    if chat_id == user_id:
        bot.reply_to(m, "❌ Chỉ có thể rải lộc trong GROUP CHAT!")
        return
    if len(parts) != 2:
        bot.reply_to(m, "⚠️ /loc [số_xu]\nVí dụ: `/loc 50000`", parse_mode="Markdown")
        return
    try:
        so_tien = int(parts[1])
    except:
        bot.reply_to(m, "⚠️ Số xu không hợp lệ")
        return
    
    khoi_tao_user(user_id)
    if users_data[user_id]["tien"] < so_tien:
        bot.reply_to(m, f"❌ Bạn không đủ {so_tien:,}đ để rải lộc!", parse_mode="Markdown")
        return
    if so_tien < 1000:
        bot.reply_to(m, "❌ Số xu rải lộc tối thiểu 1,000đ!", parse_mode="Markdown")
        return
    
    users_data[user_id]["tien"] -= so_tien
    loc_data[chat_id] = {
        "so_tien": so_tien,
        "nguoi_rai": user_id,
        "da_nhan": None,
        "thoi_gian_het_han": datetime.now() + timedelta(minutes=5),
        "so_tien_con_lai": so_tien
    }
    
    try:
        nguoi_rai = m.from_user.first_name
    except:
        nguoi_rai = str(user_id)
    
    bot.send_message(
        chat_id,
        f"🌊 **RẢI LỘC NHÓM** 🌊\n━━━━━━━━━━━━━━━━━━━━\n🎁 **{nguoi_rai}** vừa rải **{so_tien:,}đ**\n💰 CHỈ 1 NGƯỜI ĐẦU TIÊN NHẤN NÚT SẼ NHẬN TOÀN BỘ!\n⏰ Hết hạn sau 5 phút!\n━━━━━━━━━━━━━━━━━━━━\n👇 **NHẤN NÚT BÊN DƯỚI ĐỂ NHẬN TIỀN!**",
        reply_markup=menu_nhan_loc(chat_id, so_tien),
        parse_mode="Markdown"
    )
    threading.Thread(target=auto_xoa_loc, args=(chat_id,), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("nhan_loc_"))
def nhan_loc(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    loc_original_chat_id = int(call.data.split("_")[2])
    
    if chat_id != loc_original_chat_id:
        bot.answer_callback_query(call.id, "❌ Không phải lộc của group này!", show_alert=True)
        return
    if loc_original_chat_id not in loc_data:
        bot.answer_callback_query(call.id, "❌ Lộc đã hết hoặc đã hết hạn!", show_alert=True)
        try:
            bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        except:
            pass
        return
    
    loc = loc_data[loc_original_chat_id]
    
    if user_id == loc["nguoi_rai"]:
        bot.answer_callback_query(call.id, "❌ Bạn là người rải lộc, không thể nhận lại!", show_alert=True)
        return
    if loc["da_nhan"] is not None:
        bot.answer_callback_query(call.id, "❌ Lộc đã được người khác nhận rồi!", show_alert=True)
        try:
            bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
            bot.send_message(chat_id, f"⏰ **LỘC ĐÃ ĐƯỢC NHẬN!**\n━━━━━━━━━━━━━━━━━━━━\n💰 {loc['so_tien']:,}đ đã được nhận bởi người khác!", parse_mode="Markdown")
        except:
            pass
        return
    
    tien_nhan = loc["so_tien_con_lai"]
    
    khoi_tao_user(user_id)
    users_data[user_id]["tien"] += tien_nhan
    loc["da_nhan"] = user_id
    loc["so_tien_con_lai"] = 0
    
    bot.answer_callback_query(call.id, f"🎉 Bạn nhận được {tien_nhan:,}đ!", show_alert=True)
    
    try:
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except:
        pass
    
    try:
        user_nhan = bot.get_chat(user_id)
        ten_nguoi_nhan = user_nhan.first_name or str(user_id)
    except:
        ten_nguoi_nhan = str(user_id)
    
    try:
        user_rai = bot.get_chat(loc["nguoi_rai"])
        ten_nguoi_rai = user_rai.first_name or str(loc["nguoi_rai"])
    except:
        ten_nguoi_rai = str(loc["nguoi_rai"])
    
    bot.send_message(chat_id, f"🎉🎉🎉 **{ten_nguoi_nhan}** đã nhận toàn bộ lộc!\n━━━━━━━━━━━━━━━━━━━━\n💰 **{tien_nhan:,}đ** từ {ten_nguoi_rai}\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    del loc_data[loc_original_chat_id]

def auto_xoa_loc(chat_id):
    time.sleep(300)
    if chat_id in loc_data:
        loc = loc_data[chat_id]
        if loc["da_nhan"] is None and loc["so_tien_con_lai"] > 0:
            khoi_tao_user(loc["nguoi_rai"])
            users_data[loc["nguoi_rai"]]["tien"] += loc["so_tien_con_lai"]
            bot.send_message(chat_id, f"⏰ **HẾT GIỜ NHẬN LỘC!**\n━━━━━━━━━━━━━━━━━━━━\n💰 Số tiền {loc['so_tien_con_lai']:,}đ đã được hoàn trả cho người rải.", parse_mode="Markdown")
            del loc_data[chat_id]

@bot.message_handler(commands=['xemloc'])
def xem_loc(m):
    chat_id = m.chat.id
    if chat_id not in loc_data:
        bot.reply_to(m, "📭 Hiện không có lộc nào trong group này!")
        return
    loc = loc_data[chat_id]
    try:
        nguoi_rai = bot.get_chat(loc["nguoi_rai"])
        ten_nguoi_rai = nguoi_rai.first_name or str(loc["nguoi_rai"])
    except:
        ten_nguoi_rai = str(loc["nguoi_rai"])
    
    if loc["da_nhan"]:
        try:
            nguoi_nhan = bot.get_chat(loc["da_nhan"])
            ten_nguoi_nhan = nguoi_nhan.first_name or str(loc["da_nhan"])
        except:
            ten_nguoi_nhan = str(loc["da_nhan"])
        bot.reply_to(m, f"🌊 **THÔNG TIN LỘC** 🌊\n━━━━━━━━━━━━━━━━━━━━\n🎁 Người rải: {ten_nguoi_rai}\n💰 Tổng lộc: {loc['so_tien']:,}đ\n✅ Đã nhận bởi: {ten_nguoi_nhan}\n⏰ Hết hạn: {loc['thoi_gian_het_han'].strftime('%H:%M:%S')}\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    else:
        bot.reply_to(m, f"🌊 **THÔNG TIN LỘC** 🌊\n━━━━━━━━━━━━━━━━━━━━\n🎁 Người rải: {ten_nguoi_rai}\n💰 Tổng lộc: {loc['so_tien']:,}đ\n⏳ Còn lại: {loc['so_tien_con_lai']:,}đ\n👤 Chưa có ai nhận\n⏰ Hết hạn: {loc['thoi_gian_het_han'].strftime('%H:%M:%S')}\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")

@bot.message_handler(commands=['lichsuloc'])
def lich_su_nhan_loc(m):
    chat_id = m.chat.id
    if chat_id not in loc_data:
        bot.reply_to(m, "📭 Hiện không có lộc nào trong group này!")
        return
    loc = loc_data[chat_id]
    if loc["da_nhan"] is None:
        bot.reply_to(m, "📭 Chưa có ai nhận lộc!")
        return
    try:
        user = bot.get_chat(loc["da_nhan"])
        name = user.first_name or str(loc["da_nhan"])
    except:
        name = str(loc["da_nhan"])
    bot.reply_to(m, f"📊 **LỊCH SỬ NHẬN LỘC**\n━━━━━━━━━━━━━━━━━━━━\n🎉 {name} đã nhận {loc['so_tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")

# ============ LỆNH KINH TẾ ============
@bot.message_handler(commands=['kiemxu'])
def kiemxu(m):
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    today = datetime.now().date()
    if user_id in daily_kiemxu and daily_kiemxu[user_id] == today:
        bot.reply_to(m, "❌ Bạn đã kiếm xu hôm nay rồi! Quay lại ngày mai.")
        return
    thuong = random.randint(100, 200)
    users_data[user_id]["tien"] += thuong
    daily_kiemxu[user_id] = today
    bot.reply_to(m, f"💼 **KIẾM XU** 💼\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền nhận:** +{thuong}đ\n💎 **Số dư:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")

@bot.message_handler(commands=['lixi'])
def lixi(m):
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    today = datetime.now().date()
    if user_id in daily_lixi and daily_lixi[user_id] == today:
        bot.reply_to(m, "❌ Bạn đã lì xì hôm nay rồi! Quay lại ngày mai.")
        return
    thuong = random.randint(500, 9000000)
    users_data[user_id]["tien"] += thuong
    daily_lixi[user_id] = today
    bot.reply_to(m, f"🧧 **LÌ XÌ MAY MẮN** 🧧\n━━━━━━━━━━━━━━━━━━━━\n💰 **Tiền nhận:** +{thuong}đ\n💎 **Số dư:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")

@bot.message_handler(commands=['tangxu'])
def tangxu(m):
    parts = m.text.split()
    if len(parts) != 3:
        bot.reply_to(m, "⚠️ /tangxu [id] [số_xu]")
        return
    try:
        target_id = int(parts[1])
        so_tien = int(parts[2])
    except:
        bot.reply_to(m, "⚠️ ID hoặc số xu không hợp lệ")
        return
    
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    khoi_tao_user(target_id)
    
    if users_data[user_id]["tien"] < so_tien:
        bot.reply_to(m, f"❌ Bạn không đủ {so_tien:,}đ để tặng!")
        return
    if so_tien <= 0:
        bot.reply_to(m, "❌ Số xu phải lớn hơn 0")
        return
    
    users_data[user_id]["tien"] -= so_tien
    users_data[target_id]["tien"] += so_tien
    
    bot.reply_to(m, f"🤝 **TẶNG XU** 🤝\n━━━━━━━━━━━━━━━━━━━━\n📤 **Bạn tặng:** -{so_tien:,}đ\n📥 **Người nhận:** +{so_tien:,}đ\n💎 **Số dư của bạn:** {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    
    try:
        bot.send_message(target_id, f"🤝 **BẠN NHẬN ĐƯỢC XU** 🤝\n━━━━━━━━━━━━━━━━━━━━\n🎁 **Người tặng:** {m.from_user.first_name}\n💰 **Tiền nhận:** +{so_tien:,}đ\n💎 **Số dư mới:** {users_data[target_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown")
    except:
        pass

# ============ ADMIN COMMANDS ============
@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id not in ADMIN_IDS:
        bot.reply_to(m, "❌ Bạn không phải admin!")
        return
    msg = m.text.replace('/broadcast', '').strip()
    if not msg:
        bot.reply_to(m, "⚠️ /broadcast [nội dung]")
        return
    success = 0
    for uid in users_data:
        try:
            bot.send_message(uid, f"📢 **THÔNG BÁO TỪ ADMIN** 📢\n\n{msg}", parse_mode="Markdown")
            success += 1
        except:
            pass
        time.sleep(0.1)
    bot.reply_to(m, f"✅ Đã gửi broadcast đến {success} user")

@bot.message_handler(commands=['speed'])
def set_speed(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    parts = m.text.split()
    if len(parts) == 2:
        global TOC_DO_SPAM
        TOC_DO_SPAM = float(parts[1])
        bot.reply_to(m, f"⚡ Đã set speed: {TOC_DO_SPAM}s")

@bot.message_handler(commands=['spslow'])
def set_slow(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    parts = m.text.split()
    if len(parts) == 2:
        global CHE_DO_SLOW, THOI_GIAN_SLOW
        if parts[1] == "on":
            CHE_DO_SLOW = True
            bot.reply_to(m, f"🐢 Đã bật slow (+{THOI_GIAN_SLOW}s)")
        elif parts[1] == "off":
            CHE_DO_SLOW = False
            bot.reply_to(m, "⚡ Đã tắt slow")

# ============ XỬ LÝ CALLBACK CHUNG ============
@bot.callback_query_handler(func=lambda call: True)
def handle_common_callbacks(call):
    user_id = call.from_user.id
    khoi_tao_user(user_id)
    
    if call.data == "open_spam_menu":
        bot.edit_message_text(
            "⚔️ **MENU SPAM** ⚔️\n━━━━━━━━━━━━━━━━━━━━\n"
            "🔥 **/sp [ID/@user]** - Spam từ file (tag ẩn)\n"
            "💀 **/sp2 [ID/@user]** - Spam câu đặc biệt (tag ẩn)\n"
            "📝 **/spnd [ID/@user] nội dung** - Spam nội dung tự chọn (tag ẩn)\n"
            "🎨 **/spstick [ID/@user]** - Reply sticker + spam sticker (tag ẩn)\n"
            "🛑 **/stop** - Dừng tất cả spam\n"
            "🗑️ **/clearall** - Xóa 200 tin nhắn gần nhất\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📌 **CÁCH DÙNG:**\n"
            "• /sp 123456789\n"
            "• /sp2 @username\n"
            "• /spnd 8266903635 mày là thằng ngu\n"
            "• Reply sticker + /spstick 123456789\n"
            "━━━━━━━━━━━━━━━━━━━━\n👇 **Bấm nút bên dưới để quay lại:**",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_spam_chinh(), parse_mode="Markdown"
        )
    elif call.data == "open_game_menu":
        bot.edit_message_text(
            f"🎮 **MENU GAME** 🎮\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🏆 Thắng: {users_data[user_id]['thang']} | Thua: {users_data[user_id]['thua']}\n━━━━━━━━━━━━━━━━━━━━\n🎲 Tài Xỉu - Cược tài/xỉu\n🎃 Bầu Cua - Game dân gian 3 linh vật\n🎫 Vé Số - Mua số may mắn\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn game:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_game_chinh(), parse_mode="Markdown"
        )
    elif call.data == "open_admin_menu":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "❌ Bạn không phải admin!", show_alert=True)
            return
        bot.edit_message_text(
            "👑 **MENU ADMIN** 👑\n━━━━━━━━━━━━━━━━━━━━\n⚔️ SPAM - Công cụ spam\n🎮 GAME - Chơi game\n👑 ADMIN PANEL - Quản trị\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn menu:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_admin_chinh(), parse_mode="Markdown"
        )
    elif call.data == "back_to_main":
        bot.edit_message_text(
            f"🎮 **MENU CHÍNH** 🎮\n━━━━━━━━━━━━━━━━━━━━\n⚔️ SPAM - Công cụ spam\n🎮 GAME - Hệ thống game\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_chinh(), parse_mode="Markdown"
        )
    elif call.data == "back_to_game_menu":
        bot.edit_message_text(
            f"🎮 **MENU GAME** 🎮\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🏆 Thắng: {users_data[user_id]['thang']} | Thua: {users_data[user_id]['thua']}\n━━━━━━━━━━━━━━━━━━━━\n🎲 Tài Xỉu - Cược tài/xỉu\n🎃 Bầu Cua - Game dân gian 3 linh vật\n🎫 Vé Số - Mua số may mắn\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn game:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_game_chinh(), parse_mode="Markdown"
        )
    elif call.data == "back_to_admin_main":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "❌ Bạn không phải admin!", show_alert=True)
            return
        bot.edit_message_text(
            "👑 **MENU ADMIN** 👑\n━━━━━━━━━━━━━━━━━━━━\n⚔️ SPAM - Công cụ spam\n🎮 GAME - Chơi game\n👑 ADMIN PANEL - Quản trị\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn menu:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_admin_chinh(), parse_mode="Markdown"
        )
    elif call.data == "admin_panel":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "❌ Bạn không phải admin!", show_alert=True)
            return
        bot.edit_message_text(
            "👑 **ADMIN CONTROL PANEL** 👑\n━━━━━━━━━━━━━━━━━━━━\n🧧 LÌ XÌ ADMIN\n📊 THỐNG KÊ USER\n⚙️ SET SPEED - /speed\n🐢 SLOW MODE - /spslow\n📢 BROADCAST\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_admin_settings(), parse_mode="Markdown"
        )
    elif call.data == "admin_lixi":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "❌ Bạn không phải admin!", show_alert=True)
            return
        bot.edit_message_text(
            "🧧 **LÌ XÌ ADMIN** 🧧\n━━━━━━━━━━━━━━━━━━━━\nChọn số tiền muốn lì xì:\n━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_admin_lixi(), parse_mode="Markdown"
        )
    elif call.data.startswith("lixi_admin_"):
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "❌ Bạn không phải admin!", show_alert=True)
            return
        if call.data == "lixi_admin_manual":
            msg = bot.send_message(call.message.chat.id, "💰 Nhập ID user và số tiền:\nVí dụ: `123456789 500000`", parse_mode="Markdown")
            bot.register_next_step_handler(msg, xu_ly_lixi_admin_manual)
        else:
            so_tien = int(call.data.split("_")[2])
            msg = bot.send_message(call.message.chat.id, f"💰 Nhập ID user nhận lì xì {so_tien:,}đ:", parse_mode="Markdown")
            bot.register_next_step_handler(msg, xu_ly_lixi_admin, so_tien)
        bot.answer_callback_query(call.id)
    elif call.data == "admin_stats":
        tong_tien = sum(data["tien"] for data in users_data.values())
        bot.send_message(call.message.chat.id, f"📊 **THỐNG KÊ**\n👥 User: {len(users_data)}\n💰 Tổng tiền: {tong_tien:,}đ", parse_mode="Markdown")
    elif call.data == "admin_speed":
        bot.send_message(call.message.chat.id, f"⚙️ Speed: {TOC_DO_SPAM}s\nDùng /speed [số]", parse_mode="Markdown")
    elif call.data == "admin_slow":
        trang_thai = "BẬT" if CHE_DO_SLOW else "TẮT"
        bot.send_message(call.message.chat.id, f"🐢 Slow: {trang_thai}\nDùng /spslow on/off", parse_mode="Markdown")
    elif call.data == "admin_broadcast":
        bot.send_message(call.message.chat.id, "📢 Dùng /broadcast [nội dung]", parse_mode="Markdown")
    elif call.data.startswith("help_"):
        cmd = call.data.replace('help_', '')
        bot.answer_callback_query(call.id, f"📌 Lệnh: /{cmd}", show_alert=True)
    elif call.data.startswith("manual_bet_"):
        parts = call.data.split("_")
        loai = parts[2]
        user_id_cuoc = int(parts[3])
        if user_id != user_id_cuoc:
            bot.answer_callback_query(call.id, "❌ Không phải phiên của bạn!", show_alert=True)
            return
        msg = bot.send_message(call.message.chat.id, "💰 Nhập số tiền bạn muốn cược (tối thiểu 100đ):")
        bot.register_next_step_handler(msg, xu_ly_nhap_tien_cuoc, user_id, loai)
        bot.answer_callback_query(call.id)

def xu_ly_lixi_admin(message, so_tien):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Bạn không phải admin!")
        return
    target_input = message.text.strip()
    try:
        if target_input.startswith('@'):
            user_info = bot.get_chat(target_input)
            target_id = user_info.id
        else:
            target_id = int(target_input)
        khoi_tao_user(target_id)
        users_data[target_id]["tien"] += so_tien
        bot.reply_to(message, f"🧧 **LÌ XÌ ADMIN**\n✅ +{so_tien:,}đ cho `{target_id}`\n💰 Số dư mới: {users_data[target_id]['tien']:,}đ", parse_mode="Markdown")
        try:
            bot.send_message(target_id, f"🧧 **BẠN NHẬN LÌ XÌ TỪ ADMIN!**\n🎁 +{so_tien:,}đ\n💰 Số dư: {users_data[target_id]['tien']:,}đ", parse_mode="Markdown")
        except:
            pass
    except:
        bot.reply_to(message, f"❌ Không tìm thấy user: {target_input}")

def xu_ly_lixi_admin_manual(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Bạn không phải admin!")
        return
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ Sai định dạng! Dùng: `ID_user số_tiền`")
            return
        target_input, so_tien = parts[0], int(parts[1])
        if so_tien <= 0:
            bot.reply_to(message, "❌ Số tiền phải > 0")
            return
        if target_input.startswith('@'):
            user_info = bot.get_chat(target_input)
            target_id = user_info.id
        else:
            target_id = int(target_input)
        khoi_tao_user(target_id)
        users_data[target_id]["tien"] += so_tien
        bot.reply_to(message, f"🧧 **LÌ XÌ ADMIN**\n✅ +{so_tien:,}đ cho `{target_id}`\n💰 Số dư mới: {users_data[target_id]['tien']:,}đ", parse_mode="Markdown")
        try:
            bot.send_message(target_id, f"🧧 **BẠN NHẬN LÌ XÌ TỪ ADMIN!**\n🎁 +{so_tien:,}đ\n💰 Số dư: {users_data[target_id]['tien']:,}đ", parse_mode="Markdown")
        except:
            pass
    except:
        bot.reply_to(message, "❌ Sai định dạng hoặc không tìm thấy user!")

def xu_ly_nhap_tien_cuoc(message, user_id, loai):
    try:
        so_tien = int(message.text.strip())
        if so_tien < 100:
            bot.reply_to(message, "❌ Số tiền cược tối thiểu là 100đ!")
            return
        
        khoi_tao_user(user_id)
        if users_data[user_id]["tien"] < so_tien:
            bot.reply_to(message, f"❌ Bạn không đủ {so_tien:,}đ để cược!")
            return
        
        users_data[user_id]["tien"] -= so_tien
        
        msg1 = bot.send_dice(message.chat.id, emoji="🎲")
        time.sleep(0.8)
        msg2 = bot.send_dice(message.chat.id, emoji="🎲")
        time.sleep(0.8)
        msg3 = bot.send_dice(message.chat.id, emoji="🎲")
        time.sleep(1.5)
        
        dice1, dice2, dice3 = msg1.dice.value, msg2.dice.value, msg3.dice.value
        tong = dice1 + dice2 + dice3
        ket_qua = "tai" if tong >= 11 else "xiu"
        icon_map = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        
        if ket_qua == loai:
            thuong = so_tien * 2
            users_data[user_id]["tien"] += thuong
            users_data[user_id]["thang"] += 1
            bot.send_message(message.chat.id, f"🎉 **BẠN THẮNG!** 🎉\n━━━━━━━━━━━━━━━━━━━━\n🎲 {icon_map[dice1]} {icon_map[dice2]} {icon_map[dice3]}\n🔢 Tổng: {tong}\n✅ Kết quả: {ket_qua.upper()}\n━━━━━━━━━━━━━━━━━━━━\n💰 Tiền cược: -{so_tien:,}đ\n💎 Tiền thắng: +{thuong:,}đ\n📊 Lãi: +{thuong - so_tien:,}đ\n💎 Số dư: {users_data[user_id]['tien']:,}đ", parse_mode="Markdown")
        else:
            users_data[user_id]["thua"] += 1
            bot.send_message(message.chat.id, f"💀 **BẠN THUA!** 💀\n━━━━━━━━━━━━━━━━━━━━\n🎲 {icon_map[dice1]} {icon_map[dice2]} {icon_map[dice3]}\n🔢 Tổng: {tong}\n❌ Kết quả: {ket_qua.upper()}\n━━━━━━━━━━━━━━━━━━━━\n💰 Tiền cược: -{so_tien:,}đ\n💎 Tiền thắng: +0đ\n📊 Lỗ: -{so_tien:,}đ\n💎 Số dư: {users_data[user_id]['tien']:,}đ", parse_mode="Markdown")
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎲 CHƠI LẠI", callback_data="menu_roll"), InlineKeyboardButton("🔙 MENU GAME", callback_data="back_to_game_menu"))
        bot.send_message(message.chat.id, "👇 Chọn tiếp:", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "❌ Vui lòng nhập số tiền hợp lệ!")

# ============ COMMAND ============
@bot.message_handler(commands=['veso'])
def ve_so_command(m):
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    bot.reply_to(
        m,
        f"🎫 **MUA VÉ SỐ - VIETLOTT** 🎫\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n🎯 Giá vé: 10,000đ/vé\n🏆 Giải thưởng:\n   • ĐB: x100\n   • Nhất: x20\n   • Nhì: x10\n   • Ba: x5\n   • KK: x2\n⏰ Mở thưởng sau 30 giây!\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        reply_markup=menu_ve_so(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['baucua'])
def baucua_command(m):
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    cuoc_mac_dinh = user_bet_amounts.get(user_id, {}).get("baucua", 1000)
    bot.reply_to(
        m,
        f"🎃 **BẦU CUA TÔM CÁ** 🎃\n━━━━━━━━━━━━━━━━━━━━\n💰 Số tiền: {users_data[user_id]['tien']:,}đ\n💸 Tiền cược: {cuoc_mac_dinh:,}đ\n━━━━━━━━━━━━━━━━━━━━\n🐟 🦐 🦀 🐓 🌿 🐯\n━━━━━━━━━━━━━━━━━━━━\n👉 Chọn linh vật:",
        reply_markup=menu_baucua(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['topxu'])
def topxu_command(m):
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]["tien"], reverse=True)[:10]
    msg = "📊 **TOP XU** 📊\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, (uid, data) in enumerate(sorted_users, 1):
        try:
            user = bot.get_chat(uid)
            name = user.first_name or str(uid)
        except:
            name = str(uid)
        msg += f"{i}. {name}: {data['tien']:,}đ\n"
    msg += "━━━━━━━━━━━━━━━━━━━━"
    bot.reply_to(m, msg, parse_mode="Markdown")

@bot.message_handler(commands=['start', 'help', 'menu'])
def start(m):
    khoi_tao_user(m.from_user.id)
    bot.reply_to(
        m,
        f"🎮 **BOT SPAM + CASINO** 🎮\n━━━━━━━━━━━━━━━━━━━━\n🎁 Bạn được tặng **100,000đ**\n━━━━━━━━━━━━━━━━━━━━\n❓ **HƯỚNG DẪN NHANH** ❓\n🎮 /menu — Menu chính\n💼 /kiemxu — Kiếm 100-200xu\n🧧 /lixi — Lì xì 1 lần/ngày\n🤝 /tangxu [id] [xu] — Tặng xu\n🌊 /loc [xu] — Rải lộc (group)\n🎃 /baucua — Bầu cua 3 linh vật\n🎫 /veso — Mua vé số\n📊 /topxu — Top giàu\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        reply_markup=menu_chinh(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['menu'])
def show_menu(m):
    user_id = m.from_user.id
    khoi_tao_user(user_id)
    bot.reply_to(
        m,
        f"🎮 **MENU CHÍNH** 🎮\n━━━━━━━━━━━━━━━━━━━━\n💰 Số dư: {users_data[user_id]['tien']:,}đ\n━━━━━━━━━━━━━━━━━━━━\n⚔️ SPAM - Công cụ spam\n🎮 GAME - Hệ thống game\n━━━━━━━━━━━━━━━━━━━━\n👇 Chọn chức năng:",
        reply_markup=menu_chinh(),
        parse_mode="Markdown"
    )

# ============ KHỞI TẠO ============
def khoi_tao_xo_so():
    global thoi_gian_mo_thuong
    thoi_gian_mo_thuong = datetime.now() + timedelta(seconds=10)
    thread = threading.Thread(target=mo_thuong_tu_dong, daemon=True)
    thread.start()
    print("🎫 XỔ SỐ ĐÃ ĐƯỢC KHỞI TẠO! Mở thưởng sau 10 giây!")

# ============ CHẠY BOT ============
print("🚀 BOT ĐANG CHẠY...")
print("⚡ Made by Lyx Ai - Zamzzz Creation")
print("🎮 Đã xóa vòng quay | Lộc chỉ 1 người nhận | Bầu cua random 3 sticker")
print("📝 Menu spam đã chuyển sang text | Spam dùng ID tag ẩn")
khoi_tao_xo_so()
bot.infinity_polling()