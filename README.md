1. Download this file http://vision.ucas.ac.cn/resource/tiny_set.zip

2. Extract to "data" folder so it looks something like this
    ```
       data
       |-- coco
       |__ tiny_set
           |__ annotations
           |__ erase_with_uncertain_dataset
           |__ left
           |__ test
           |__ train
    ```

3. Download file tiny_set_test_nobox.json from this link and copy to data/tiny_set/annotations/erase_with_uncertain_dataset/annotations
    ```
    https://drive.google.com/file/d/1tKl2oX10stHcKKFgKUQpHtplQ93xedV9/view?usp=sharing
    ```

4. Execute
    ```
    conda env create -f environment.yml
    conda activate CenterNet
    pip install -r requirements.txt
    ```
5. Compile DCNv2
    ```
    cd src/lib/models/networks
    git clone https://github.com/CharlesShang/DCNv2
    cd DCNv2
    ./make.sh
    ```
6. Have a look at the following file for loading TinyPerson dataset
    ```
    src/lib/datasets/dataset/tiny.py
    ```
7. Run train 
    ```
    python src/main.py ctdet_tiny --dataset tiny --batch_size 12 --num_epochs 5 --val_intervals 1
    ```

8. Generate new COCO file for "tiny_set_test_nobox.json". The new COCO file is to generate sub images by adding "corner" property (similar to the way sub-images are generated in the train annotation file)

    ```
    python src/split_images.py
    ```  
9. Run test 
    ```
    python src/test.py ctdet_tiny --dataset tiny --trainval --load_model exp/ctdet_tiny/default/model_100.pth
    ```

10. The test result is for the new COCO file generated from step 8 so we have to merge it back to the original COCO test file
   ```
   python src/merge_results.py
   ```   
