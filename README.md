# Introduction

Django + MySQL 기반 맛집 추천 웹 애플리케이션입니다.
Elastic Beanstalk을 이용해 AWS에 배포합니다.

## 프로젝트 구조

AIRestaurant/
├── proj/ # Django 설정 모듈
├── restaurant/ # 앱
├── templates/ # 템플릿 HTML
├── .env # 환경변수 파일 (Git에 업로드 금지)
├── requirements.txt # 설치 패키지 목록
└── manage.py

## Preparation

가상 환경 설정 (WSL/macOS 공통)

```zsh
cd AIRestaurant
python3 -m venv venv
source venv/bin/activate
```

패키지 설치

```zsh
pip install -r requirements.txt
```

환경 변수 설정(.env)

```
PRODUCTION=1
DB_NAME=product_db
DB_USER=db_user
DB_PASSWORD=your_password
DB_HOST=your-db.xxxxx.rds.amazonaws.com
S3_BUCKET=your-s3-bucket-name
```

AWS CLI 설치
https://aws.amazon.com/ko/cli/

EB CLI 설치 (WSL)
WSL (Ubuntu 환경):

```
pip install --upgrade pip
pip install awsebcli --upgrade --user
```

EB CLI 설치 (macOS)
macOS (Homebrew 사용):

```
brew install awsebcli
```

## AWS 준비

- EC2 가 사용할 보안그룹을 하나 준비하고 해당 보안그룹아이디를 이용하여 EB 환경을 생성해야 합니다.
- RDS 인스턴스를 하나 생성하고 외부 접속을 허용한 다음 EC2가 사용할 보안그룹에도 MySQL 접속을 허용해줍니다.
- IAM에서 `aws-elasticbeanstalk-ec2-role` 에 S3 Full Access 등 해당 버킷의 쓰기 권한을 얼여줘야 합니다.


## Git

Git 설치
https://git-scm.com/book/ko/v2/시작하기-Git-설치

설치 후에

```zsh
git init

git add .

git commit -m "Initial Commit"
```

## Deployment

```zsh
eb init

# 설정내용
eb create \
 --vpc.id VPCID \
 --vpc.securitygroups 보안그룹ID \
 --vpc.ec2subnets 서브넷ID,서브넷ID... \
 --envvars DB_NAME=product_db,DB_USER=db_user,DB_PASSWORD=마스타암호,DB_HOST=DB엔드포인트,S3_BUCKET=버킷이름 \
 --vpc.elbpublic \
 --vpc.publicip


#  eb create \
#  --vpc.id vpc-078a5406b51b61a90 \
#  --vpc.securitygroups sg-0fa6d2c29e9cb8f63 \
#  --vpc.ec2subnets subnet-0aef092ddd766bb5f,subnet-012c0742f20a693d3,subnet-0c9149f519d6231e1,subnet-075377c222032771e \
#  --envvars DB_NAME=restaurant_db,DB_USER=admin,DB_PASSWORD=4nmfmoX7QBdZMHKFTNQU,DB_HOST=airest-d.cfwgaqsu2fpk.ap-northeast-2.rds.amazonaws.com,S3_BUCKET=airest-dev \
#  --vpc.elbpublic \
#  --vpc.publicip
```
