# No.4 backend
세계적인 명품 브랜드 [샤넬](https://www.chanel.com/ko_KR/)의 한국 공식 홈페이지를 클론 했습니다.
한국 홈페이지는 로그인 기능이 없어 US샤넬의 로그인을 클론하였습니다.
 - 기간 : 2주
 - 팀원구성
   - Frontend : 3명
   - Backend : 3명

Frontend의 깃허브는 [여기](https://github.com/wecode-bootcamp-korea/9-No.4-frontend)를 참고해주세요

## Demo
![](https://images.velog.io/images/yongineer1990/post/e7150a22-cc60-4fbe-abb4-b1bed5ca682e/image.png)
[영상 보기](https://youtu.be/xal1C8M6V0g)

## 적용 기술 (Backend)

- Python
- Django
- Beautifulsoup
- Selenium
- Bcrypt
- JWT
- Mysql
- CORS headers

## Modeling
![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/1bfc3a2e-92ae-4fdd-a64b-3e5aea3d1ca9/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200704%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200704T144450Z&X-Amz-Expires=86400&X-Amz-Signature=bb64bc2a2f11dbc8c14b3c8e14e95d7caab6418b3fc2bcdf153a65e5ed132f4f&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)
## 구현 기능
### 회원가입
- Frontend에서 전달받은 사용자 정보를 User 테이블에 저장합니다.
- Password는 암호화(Bycrpt)과정을 거칩니다.
### 로그인
- Frontend에서 전달받은 사용자 정보가 User 테이블에 저장된 사용자인지 검증합니다.
- 로그인 성공시 JWT Access Token을 발급합니다.
### 모든 룩 보기
- 해당 컬렉션의 모든 Look의 정보를 Frontend에게 전송합니다.
  - 대표 이미지
  - id
### 룩 정보 보기
- 해당 Look에 포함된 모든 Product에 대한 상세정보를 전송합니다.
  - id
  - 이름
  - 제품코드
  - 가격
  - 색상
  - 재질
- 해당 Look의 모든 이미지를 전송합니다.
### 카테고리별 룩 필터링
- 해당 카테고리의 제품이 포함된 룩을 필터링하여 전송합니다.
### 모든 제품 보기 (가방)
- 해당 카테고리의 모든 제품에 대한 정보를 전송합니다.
  - 제품 코드
  - 이름
  - 가격
  - 대표 이미지
  - 재질
### 제품 상세보기
- 해당 제품의 상세보기 정보를 전송합니다.
  - 모든 제품 이미지
  - 재질
  - 사이즈 (cm)
  - 사이즈 (in)
  - 색상
  - 제품 코드
  - 이름
  - 옵션의 개수
  - 옵션에 따른 제품 코드
  - 옵션에 따른 제품 이미지
### 위시리스트 추가 및 삭제
- 사용자가 선택한 Look 또는 Product를 Wishlist 테이블에 저장합니다.
- 저장시 JWT Access Token을 이용하여 해당 사용자가 회원인지 검증합니다.
### 위시리스트 정보
- 위시리스트 페이지 접속시 해당 유저가 선택한 Look과 Product 의 위시리스트를 취합하여 전송합니다.
  - Look
    - 컬렉션 ID
    - 컬렉션 이름
    - 룩 ID
    - 이름
    - 대표 이미지
  - Product
    - 제품 ID
    - 제품 이름
    - 가격
    - 재질
    - 대표 이미지
- 전달하는 과정에서 JWT Access Token을 이용하여 해당 유저가 저장한 위시리스트만 전달합니다.
## API Documentation
[Postman Documentation](https://documenter.getpostman.com/view/11684511/T17Ge7NY?version=latest)