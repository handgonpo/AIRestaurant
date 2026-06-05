# AI Restaurant

Django + MySQL 기반 맛집 추천 웹 애플리케이션입니다.  
AWS Elastic Beanstalk을 이용해 배포합니다.

---

## 1. 프로젝트 소개

이 프로젝트는 Django 기반의 맛집 추천 웹 애플리케이션입니다.

주요 구성은 다음과 같습니다.

- Django 기반 웹 애플리케이션
- MySQL / AWS RDS 연동
- AWS S3를 이용한 정적 파일 및 미디어 파일 관리
- AWS Elastic Beanstalk을 이용한 배포
- 환경변수 기반 운영 설정 관리

---

## 2. 프로젝트 구조

```text
AIRestaurant/
├── proj/                 # Django 설정 모듈
├── restaurant/           # restaurant 앱
├── templates/            # 템플릿 HTML
├── .env                  # 환경변수 파일, Git 업로드 금지
├── requirements.txt      # 설치 패키지 목록
└── manage.py
```

---

## 3. 로컬 개발 환경 준비

### 3-1. 프로젝트 폴더 이동

```zsh
cd AIRestaurant
```

### 3-2. 가상환경 생성 및 활성화

WSL / macOS 공통입니다.

```zsh
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell을 사용하는 경우:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3-3. 패키지 설치

```zsh
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```text
PRODUCTION=1
DB_NAME=product_db
DB_USER=db_user
DB_PASSWORD=your_password
DB_HOST=your-db.xxxxx.rds.amazonaws.com
S3_BUCKET=your-s3-bucket-name
```

`.env` 파일은 절대 GitHub에 업로드하면 안 됩니다.

`.gitignore`에 아래 내용이 포함되어 있어야 합니다.

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 5. AWS 사전 준비

Elastic Beanstalk 배포 전에 아래 항목을 준비합니다.

### 5-1. RDS 생성

AWS RDS에서 MySQL 인스턴스를 생성합니다.

준비해야 할 값은 다음과 같습니다.

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
```

예시:

```text
DB_NAME=restaurant_db
DB_USER=admin
DB_PASSWORD=your_rds_password
DB_HOST=your-rds-endpoint.ap-northeast-2.rds.amazonaws.com
```

### 5-2. S3 버킷 생성

정적 파일 또는 미디어 파일 저장을 위해 S3 버킷을 생성합니다.

예시:

```text
S3_BUCKET=airest-dev
```

### 5-3. 보안그룹 설정

Elastic Beanstalk의 EC2 인스턴스가 RDS에 접속할 수 있도록 보안그룹을 설정해야 합니다.

확인할 항목은 다음과 같습니다.

- Elastic Beanstalk에서 사용할 EC2 보안그룹 생성
- RDS 보안그룹의 인바운드 규칙에 MySQL 포트 허용
- MySQL 포트: `3306`
- 소스는 Elastic Beanstalk EC2 보안그룹으로 지정

예시:

```text
Type: MySQL/Aurora
Port: 3306
Source: Elastic Beanstalk EC2 Security Group
```

### 5-4. IAM 권한 설정

Elastic Beanstalk EC2 인스턴스 역할에 S3 접근 권한을 부여합니다.

확인할 역할 예시:

```text
aws-elasticbeanstalk-ec2-role
```

필요한 권한 예시:

```text
AmazonS3FullAccess
```

실무에서는 전체 권한보다 해당 버킷에만 접근 가능한 정책을 사용하는 것이 더 안전합니다.

---

## 6. AWS CLI 설치

AWS CLI 설치 문서:

```text
https://aws.amazon.com/ko/cli/
```

설치 후 AWS 계정을 설정합니다.

```zsh
aws configure
```

입력 항목:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

서울 리전을 사용하는 경우:

```text
ap-northeast-2
```

---

## 7. EB CLI 설치

### 7-1. WSL / Ubuntu

```zsh
pip install --upgrade pip
pip install awsebcli --upgrade --user
```

설치 확인:

```zsh
eb --version
```

만약 `eb` 명령어를 찾을 수 없다고 나오면 PATH 설정이 필요할 수 있습니다.

```zsh
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

다시 확인합니다.

```zsh
eb --version
```

### 7-2. macOS

```zsh
brew install awsebcli
```

설치 확인:

```zsh
eb --version
```

---

## 8. Git 설정

Git 설치 문서:

```text
https://git-scm.com/book/ko/v2/시작하기-Git-설치
```

프로젝트 루트에서 Git을 초기화합니다.

```zsh
git init
git add .
git commit -m "Initial commit"
```

주의할 점:

```zsh
git status
```

명령어로 `.env`가 Git에 포함되지 않았는지 반드시 확인합니다.

---

## 9. Elastic Beanstalk 초기화

프로젝트 루트에서 실행합니다.

```zsh
eb init
```

진행 중 선택할 내용은 프로젝트 상황에 맞게 입력합니다.

예시 흐름:

```text
Region: ap-northeast-2
Application name: airestaurant
Platform: Python
SSH 설정: 필요 시 yes
```

---

## 10. Elastic Beanstalk 환경 생성

아래 명령어는 Elastic Beanstalk 환경을 생성하는 명령어입니다.

```zsh
eb create \
  --vpc.id VPC_ID \
  --vpc.securitygroups SECURITY_GROUP_ID \
  --vpc.ec2subnets SUBNET_ID_1,SUBNET_ID_2,SUBNET_ID_3 \
  --envvars DB_NAME=restaurant_db,DB_USER=admin,DB_PASSWORD=your_password,DB_HOST=your-rds-endpoint.ap-northeast-2.rds.amazonaws.com,S3_BUCKET=your-s3-bucket-name \
  --vpc.elbpublic \
  --vpc.publicip
```

각 항목의 의미는 다음과 같습니다.

| 항목 | 설명 |
| --- | --- |
| `--vpc.id` | Elastic Beanstalk이 사용할 VPC ID |
| `--vpc.securitygroups` | EC2 인스턴스에 연결할 보안그룹 ID |
| `--vpc.ec2subnets` | EC2가 생성될 서브넷 ID 목록 |
| `--envvars` | 배포 환경에서 사용할 환경변수 |
| `--vpc.elbpublic` | 로드밸런서를 public으로 생성 |
| `--vpc.publicip` | EC2 인스턴스에 public IP 할당 |

---

## 11. 배포 예시 명령어

아래는 예시입니다.  
실제 비밀번호나 민감정보는 README에 그대로 작성하지 않는 것이 좋습니다.

```zsh
eb create \
  --vpc.id vpc-xxxxxxxxxxxxxxxxx \
  --vpc.securitygroups sg-xxxxxxxxxxxxxxxxx \
  --vpc.ec2subnets subnet-xxxxxxxxxxxxxxxxx,subnet-yyyyyyyyyyyyyyyyy,subnet-zzzzzzzzzzzzzzzzz \
  --envvars DB_NAME=restaurant_db,DB_USER=admin,DB_PASSWORD=your_password,DB_HOST=your-rds-endpoint.ap-northeast-2.rds.amazonaws.com,S3_BUCKET=airest-dev \
  --vpc.elbpublic \
  --vpc.publicip
```

---

## 12. 배포 후 명령어

배포 상태 확인:

```zsh
eb status
```

배포 로그 확인:

```zsh
eb logs
```

환경 열기:

```zsh
eb open
```

변경사항 재배포:

```zsh
git add .
git commit -m "Update project"
eb deploy
```

---

## 13. Django 배포 체크리스트

배포 전에 아래 항목을 확인합니다.

- `.env`가 Git에 올라가지 않았는지 확인
- `requirements.txt`가 최신인지 확인
- `ALLOWED_HOSTS`에 EB 도메인이 포함되어 있는지 확인
- `DEBUG=False` 또는 운영환경에 맞는 설정 적용
- RDS 보안그룹에서 EB EC2 보안그룹의 MySQL 접속 허용
- S3 버킷 권한 확인
- `collectstatic` 설정 확인
- `Procfile` 존재 여부 확인
- `gunicorn` 설치 여부 확인

---

## 14. 자주 발생하는 문제

### 14-1. RDS 연결 실패

확인할 것:

- `DB_HOST`가 정확한지 확인
- RDS가 public 접근 가능한지 확인
- RDS 보안그룹에서 EB EC2 보안그룹을 허용했는지 확인
- MySQL 포트 `3306`이 열려 있는지 확인

### 14-2. 정적 파일이 안 보이는 경우

확인할 것:

- `STATIC_ROOT` 설정 확인
- `collectstatic` 실행 여부 확인
- S3 설정 확인
- IAM Role에 S3 접근 권한이 있는지 확인

### 14-3. EB 환경 생성 실패

확인할 것:

- VPC ID 확인
- Subnet ID 확인
- Security Group ID 확인
- IAM Role 권한 확인
- EB CLI가 올바른 AWS 계정으로 연결되어 있는지 확인

### 14-4. 환경변수 오류

확인할 것:

```zsh
eb printenv
```

환경변수 수정:

```zsh
eb setenv DB_NAME=restaurant_db DB_USER=admin DB_PASSWORD=your_password DB_HOST=your-rds-endpoint.ap-northeast-2.rds.amazonaws.com S3_BUCKET=airest-dev
```

---

## 15. 보안 주의사항

아래 정보는 GitHub에 업로드하면 안 됩니다.

- `.env`
- DB 비밀번호
- AWS Access Key
- AWS Secret Key
- RDS 엔드포인트가 포함된 민감한 운영 설정
- S3 비공개 버킷 접근 키

민감정보가 이미 GitHub에 올라갔다면, 파일을 삭제하는 것만으로는 부족합니다.  
반드시 해당 비밀번호와 키를 새로 발급하거나 변경해야 합니다.
