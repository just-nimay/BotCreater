#!/usr/bin/env python 
# coding: utf-8

# Import required libraries
from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random
from progressbar import progressbar

from bot_creater import bot, dp
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import db

import warnings

import shutil

import markups as nav

warnings.simplefilter(action='ignore', category=FutureWarning)

CONFIG = None

async def create_zip(path, col_name, message):
    path =f'{path}/output/edition {col_name}'
    file_dir = os.listdir(path)

    print('mading arhive...')
    shutil.make_archive(col_name, 'zip', path)
    print('arhive is maded!')
    await bot.send_document(message.from_user.id, open(f'{col_name}.zip', 'rb'))
    print('arhive was send!')

# Parse the configuration file and make sure it's valid
def parse_config(path):
    
    # Input traits must be placed in the assets folder. Change this value if you want to name it something else.
    assets_path = f'{path}/assets'

    # Loop through all layers defined in CONFIG
    for layer in CONFIG:
        # Go into assets/ to look for layer folders
        layer_path = os.path.join(assets_path, layer['directory'])
        
        # Get trait array in sorted order
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])

        # If layer is not required, add a None to the start of the traits array
        if not layer['required']:
            traits = [None] + traits
        
        # Generate final rarity weights
        if layer['rarity_weights'] is None:
            rarities = [1 for x in traits]
        elif layer['rarity_weights'] == 'random':
            rarities = [random.random() for x in traits]
        elif type(layer['rarity_weights'] == 'list'):
            assert len(traits) == len(layer['rarity_weights']), "Make sure you have the current number of rarity weights"
            rarities = layer['rarity_weights']
        else:
            raise ValueError("Rarity weights is invalid")
        
        rarities = get_weighted_rarities(rarities)
        
        # Re-assign final values to main CONFIG
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        layer['traits'] = traits


# Weight rarities and return a numpy array that sums up to 1
def get_weighted_rarities(arr):
    return np.array(arr)/ sum(arr)

# Generate a single image given an array of filepaths representing layers
def generate_single_image(filepaths, path, output_filename=None):
    
    # Treat the first layer as the background
    bg = Image.open(os.path.join(path, 'assets', filepaths[0]))
    
    
    # Loop through layers 1 to n and stack them on top of another
    for filepath in filepaths[1:]:
        if filepath.endswith('.png'):
            img = Image.open(os.path.join(path, 'assets', filepath))
            bg.paste(img, (0,0), img)
    
    # Save the final image into desired location
    if output_filename is not None:
        bg.save(output_filename)
    else:
        # If output filename is not specified, use timestamp to name the image and save it in output/single_images
        if not os.path.exists(os.path.join(path, 'output', 'single_images')):
            os.makedirs(os.path.join(path, 'output', 'single_images'))
        bg.save(os.path.join(path, 'output', 'single_images', str(int(time.time())) + '.png'))


# Generate a single image with all possible traits
# generate_single_image(['Background/green.png', 
#                        'Body/brown.png', 
#                        'Expressions/standard.png',
#                        'Head Gear/std_crown.png',
#                        'Shirt/blue_dot.png',
#                        'Misc/pokeball.png',
#                        'Hands/standard.png',
#                        'Wristband/yellow.png'])


# Get total number of distinct possible combinations
def get_total_combinations():
    
    total = 1
    for layer in CONFIG:
        total = total * len(layer['traits'])
    return total


# Select an index based on rarity weights
def select_index(cum_rarities, rand):
    
    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i+1]:
            return i
    
    # Should not reach here if everything works okay
    return None


# Generate a set of traits given rarities
def generate_trait_set_from_config():
    
    trait_set = []
    trait_paths = []
    
    for layer in CONFIG:
        # Extract list of traits and cumulative rarity weights
        traits, cum_rarities = layer['traits'], layer['cum_rarity_weights']

        # Generate a random number
        rand_num = random.random()

        # Select an element index based on random number and cumulative rarity weights
        idx = select_index(cum_rarities, rand_num)

        # Add selected trait to trait set
        trait_set.append(traits[idx])

        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)
        
    return trait_set, trait_paths


# Generate the image set. Don't change drop_dup
async def generate_images(edition, count, path, message, drop_dup=True):
    
    # Initialize an empty rarity table
    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer['name']] = []

    # Define output path to path/output/edition {edition_num}
    op_path = os.path.join(path, 'output', 'edition ' + str(edition), 'images')

    # Will require this to name final images as 000, 001,...
    zfill_count = len(str(count - 1))
    
    # Create output directory if it doesn't exist
    if not os.path.exists(op_path):
        os.makedirs(op_path)
      
    # Create the images
    bar = ''
    procent = 0
    for n in progressbar(range(count)):
        numb_procent = round(100 / count)
        count_procent = round(10 / 100 * numb_procent)
        item = '|'
        progres = item * count_procent
        bar = bar[:0] + progres + bar[:-len(progres)]
        procent = procent + round(numb_procent)
        await bot.edit_message_text(f'{procent}% {bar}', message.from_user.id, message.message_id -1)
        # Set image name
        image_name = str(n).zfill(zfill_count) + '.png'
        
        # Get a random set of valid traits based on rarity weights
        trait_sets, trait_paths = generate_trait_set_from_config()

        # Generate the actual image
        generate_single_image(trait_paths, path, os.path.join(op_path, image_name))
        
        # Populate the rarity table with metadata of newly created image
        for idx, trait in enumerate(trait_sets):
            if trait is not None:
                rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
            else:
                rarity_table[CONFIG[idx]['name']].append('none')
    
    # Create the final rarity table by removing duplicate creat
    rarity_table = pd.DataFrame(rarity_table).drop_duplicates()
    print("Generated %i images, %i are distinct" % (count, rarity_table.shape[0]))

    
    if drop_dup:

        # Get list of duplicate images
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))

        #Remove duplicate images
        print("Removing %i images..." % (len(img_tb_removed)))

        #op_path = os.path.join('output', 'edition ' + str(edition))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + '.png'))

        # Rename images such that it is sequentialluy numbered
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, str(idx).zfill(zfill_count) + '.png'))
    
    
    # Modify rarity table to reflect removals
    rarity_table = rarity_table.reset_index()
    rarity_table = rarity_table.drop('index', axis=1)
    return rarity_table


# Main function. Point of entry


EDITION_NAME = None 
PAHT = None
TELEGRAM_ID = None

class FormCountImage(StatesGroup):
    get_count = State()

@dp.message_handler(state=FormCountImage.get_count)
async def get_count(message: types.Message, state: FSMContext):
    count = message.text
    try:
        count = int(count)
        if count <= 0:
            await message.answer(text=f'{count} не больше нуля!')
        else:
            await task(EDITION_NAME, count, PAHT, message)
            await create_zip(PAHT, EDITION_NAME, message)
            await bot.send_message(message.from_user.id, 'Вот, можешь скачать свои изображения с метаданными\n', reply_markup=nav.mainMenu)

            await state.finish()
            path = PAHT.split('/')
            path = path[0]
            shutil.rmtree(path)
            os.remove(f'{EDITION_NAME}.zip')

    except ValueError:
        await message.answer(text='Нужно число!')


async def task(edition_name, num_avatars, path, message):
    print("Starting task...")
    rt = await generate_images(edition_name, num_avatars, path, message)
    print("Saving metadata...")
    rt.to_csv(os.path.join(path, 'output', 'edition ' + str(edition_name), 'metadata.csv'))
    print("Task complete!")


async def main(path, edition_name, config, message):
    global CONFIG
    print(f"{'=' * 28}\n{config}\n{'-' * 28}\nTYPE: {type(config)}")
    CONFIG =config
    global EDITION_NAME
    EDITION_NAME = edition_name
    global PAHT
    PAHT = path
    
       
    
    print("Checking assets...")
    parse_config(path)
    print("Assets look great! We are good to go!")
    print()

    tot_comb = get_total_combinations()
    print("You can create a total of %i distinct avatars" % (tot_comb))
    await bot.send_message(message.from_user.id, f'Сейчас ты сможешь сделать {tot_comb} картинок всего')
    print()

    print("How many avatars would you like to create? Enter a number greater than 0: ")
    await bot.send_message(message.from_user.id, 'Сколько аватаров тебе нужно создать? Введи число, большее 0:')
    await FormCountImage.get_count.set() 




