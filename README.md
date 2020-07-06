1 . Download this file http://vision.ucas.ac.cn/resource/tiny_set.zip

2 . Extract to "data" folder so it looks something like this
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
3 . Execute
```
conda env create -f environment.yml
conda activate CenterNet
pip install -r requirements.txt
```

4 . Compile DCNv2
```
cd src/lib/models/networks
git clone https://github.com/CharlesShang/DCNv2
cd DCNv2
./make.sh
```

5 . Have a look at the following file for loading TinyPerson dataset
```
src/lib/datasets/dataset/tiny.py
```

6 . Run train 

```
python src/main.py ctdet --dataset tiny --batch_size 12
```