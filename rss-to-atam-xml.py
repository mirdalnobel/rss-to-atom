import streamlit as st
import feedparser
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

def convert_rss_to_atom(rss_url):
    # Membaca RSS feed
    feed = feedparser.parse(rss_url)

    # Membuat elemen root untuk Atom feed
    atom_feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')

    # Menambahkan elemen-elemen umum Atom feed
    title = ET.SubElement(atom_feed, 'title')
    title.text = feed.feed.title

    subtitle = ET.SubElement(atom_feed, 'subtitle')
    subtitle.text = feed.feed.subtitle if 'subtitle' in feed.feed else ''

    link = ET.SubElement(atom_feed, 'link', {'href': feed.feed.link})

    updated = ET.SubElement(atom_feed, 'updated')
    updated.text = feed.feed.updated

    # Mengonversi setiap entri RSS ke entri Atom
    for entry in feed.entries:
        atom_entry = ET.SubElement(atom_feed, 'entry')

        entry_title = ET.SubElement(atom_entry, 'title')
        entry_title.text = entry.title

        entry_link = ET.SubElement(atom_entry, 'link', {'href': entry.link})

        entry_id = ET.SubElement(atom_entry, 'id')
        entry_id.text = entry.id

        entry_updated = ET.SubElement(atom_entry, 'updated')
        entry_updated.text = entry.updated

        content = ET.SubElement(atom_entry, 'content', {'type': 'html'})
        content.text = BeautifulSoup(entry.summary, 'html.parser').get_text()

    # Membuat objek ElementTree dan menyimpannya ke file
    atom_tree = ET.ElementTree(atom_feed)
    atom_tree.write('converted_atom.xml', encoding='utf-8', xml_declaration=True)

    return 'converted_atom.xml'

# Streamlit app
st.title('RSS to Atom Converter')

# Input URL RSS feed dari pengguna
rss_url = st.text_input('Masukkan URL RSS feed:')
if st.button('Konversi ke Atom XML'):
    if rss_url:
        st.info('Proses konversi sedang berlangsung...')
        result_file = convert_rss_to_atom(rss_url)
        st.success(f'Konversi selesai! [Download File](sandbox:/converted_atom.xml)')
