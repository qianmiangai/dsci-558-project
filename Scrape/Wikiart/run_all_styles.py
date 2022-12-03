import os 

style_list = ['conceptual-art', 'minimalism', 'post-minimalism', 'light-and-space', 'environmental-land-art', 'junk-art', 'cyber-art', 'photorealism', 'hyper-realism', 'poster-art-realism', 'contemporary-realism', 'p-d-pattern-and-decoration', 'transavantgarde', 'confessional-art', 'new-european painting', 'neo-pop-art', 'neo-geo', 'maximalism', 'neo-orthodoxism', 'graffiti-art', 'street-art', 'lowbrow-art', 'stuckism', 'new-casualism', 'art-singulier', 'superflat', 'excessivism', 'digital-art', 'hyper-mannerism-anachronism', 'neo-minimalism', 'fantasy-art', 'sky-art', 'contemporary', 'site-specific-art', 'new-media-art', 'classical-realism', 'postcolonial-art', 'queer-art']

if __name__ == "__main__":
    i = 0
    os.system("mkdir output")
    for style in style_list:
        os.system(f"python3 wikiart_scraper.py --style {style} --output_dir output --num_pages 3")
