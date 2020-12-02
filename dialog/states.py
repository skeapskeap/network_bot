from telegram.ext import MessageHandler, Filters
import dialog
import dialog.asterisk as ast
import dialog.ups as ups
import dialog.ping as ping
import dialog.switch as sw

to_menu = MessageHandler(Filters.regex('^menu$'), dialog.main_menu)


def back_to(func):
    return MessageHandler(Filters.regex('^back$'), func)


main_menu = [
    MessageHandler(Filters.regex('^switch$'), sw.dialog),
    MessageHandler(Filters.regex('^UPS$'), ups.dialog),
    MessageHandler(Filters.regex('^ping$'), ping.dialog),
    MessageHandler(Filters.regex('^asterisk$'), ast.start)]

switch_ip = [
    to_menu,
    MessageHandler(Filters.regex('^switch_search$'), sw.search),
    MessageHandler(Filters.text, sw.set_ip)]

switch_search = [
    to_menu,
    back_to(sw.dialog),
    MessageHandler(Filters.text, sw.run_search)]

switch_port = [
    to_menu,
    MessageHandler(Filters.regex('^change_ip$'), sw.dialog),
    MessageHandler(Filters.text, sw.set_port)]

switch_commands = [
    to_menu,
    MessageHandler(Filters.regex('^change_ip$'), sw.dialog),
    MessageHandler(Filters.regex('^change_port$'), sw.set_ip),
    MessageHandler(Filters.regex('^sh_port$'), sw.run_command),
    MessageHandler(Filters.regex('^sh_mac$'), sw.run_command),
    MessageHandler(Filters.regex('^cab_diag$'), sw.run_command),
    MessageHandler(Filters.regex('^stats$'), sw.port_stats)]

switch_port_stats = [
    back_to(sw.back_to_commands),
    MessageHandler(Filters.regex('^refresh$'), sw.port_stats),
    MessageHandler(Filters.regex('^reset$'), sw.clear_stats)]

ping_ip = [
    to_menu,
    MessageHandler(Filters.regex('^change_ip$'), ping.dialog),
    MessageHandler(Filters.regex('^ping_again$'), ping.run),
    MessageHandler(Filters.text, ping.set_ip)]

ups_ip = [
    to_menu,
    MessageHandler(Filters.text, ups.set_ip)]

ups_actions = [
    to_menu,
    MessageHandler(Filters.regex('^change_ip$'), ups.dialog),
    MessageHandler(Filters.regex('^refresh$'), ups.actions)]

asterisk_menu = [
    to_menu,
    MessageHandler(Filters.regex('^firewall$'), ast.firewall)]

asterisk_fw = [
    to_menu,
    back_to(ast.start),
    MessageHandler(Filters.regex('^search$'), ast.search_ip),
    MessageHandler(Filters.regex('^add_ip$'), ast.add_start),
    MessageHandler(Filters.regex('^remove_ip$'), ast.del_start)]

asterisk_fw_search = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.text, ast.run_search)]

asterisk_fw_add_ip = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.text, ast.add_ip)]

asterisk_fw_add_client = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.text, ast.add_client)]

asterisk_fw_add_url = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.text, ast.add_url)]

asterisk_fw_add_commit = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.regex('^confirm$'), ast.add_commit)]

asterisk_fw_del_ip = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.text, ast.del_ip)]

asterisk_fw_del_commit = [
    to_menu,
    back_to(ast.firewall),
    MessageHandler(Filters.regex('^confirm$'), ast.del_commit)]
