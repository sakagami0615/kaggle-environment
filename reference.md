# reference

## Kaggle API

### download dataset

```bash
COMPE_NAME=titanic

INPUT_DIRPATH=../../input/${COMPE_NAME}

kaggle c download -c ${COMPE_NAME} -p ${INPUT_DIRPATH}/
```

### submit

```bash
COMPE_NAME=titanic
EXP_NAME=exp001
SUBMIT_CSV_PATH=../../result/${EXP_NAME}/submission.csv

kaggle competitions submit -c ${COMPE_NAME} -f ${SUBMIT_CSV_PATH} -m test
```

### help

```bash
kaggle c -h
```
