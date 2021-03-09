# 스네이크 게임

### 명령어 순서
1. pipenv shell => 가상환경 실행
2. pip install pygame => pygame설치
3. python snake.py => 게임 실행

![snake_game](https://user-images.githubusercontent.com/61821825/110465312-98a34580-8117-11eb-9ea7-7f890647ff1c.gif)

## 구현
  ### 1. 클래스를 통한 직관적 구조


    `python 클래스 사용
    class MAIN:
        pass
    class SNAKE:
        pass
    class FRUIT:
        pass`

  ### 2. pygame 라이브러리 내부의 기능
      - 좌표를 그려주기위한 Vector
      - 스크린 표현
      - 이동 하는 것을 보여주기 위해 새로운 요소를 다른 위치에 그려줌

  ### 3. 뱀을 표현하기 위해 이미지를 사용
      - 머리의 방향을 계산하고 새로운 이미지를 그려줌
      - 몸통의 방향을 수직, 수평으로 나눠서 계산
      - 꼬리의 방향을 계산하고 새로운 이미지를 그려줌

    => 앞쪽의 블럭(x,y)과 뒤쪽의 블럭(x,y) 좌표를 비교하여 현재 어느 방향으로 움직이고 있는지 알 수 있다.

