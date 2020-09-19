# week3 - CPP, kotlin



이번 주에 배운 내용들은 다음과 같습니다.

C++

- 키워드
  - constexpr: constexpr 키워드를 앞에 붙이면, 컴파일 시에 계산을 해서 넣음
    함수, 변수 둘 다 사용 가능

- 코딩 스타일
  - public 우선, private 나중
  - 멤버 변수는 m을 붙여서

- 파일 입출력

  - C++ 스타일

    ```c++
    ifstream fin;
    fin.open("HelloWorld.txt");
    
    char character;
    while(true)
    {
        fin.get(character);
        if(fin.fail()) // character로 못 읽어오는 문자는 없기 때문에, fail을 만났다는 것은 EOF를 만난 것
        {
            break;
        }
        cout << character;
    }
    
    fin.close();
    ```

    

- 다형성

  - C++에서 다형성은 상속을 함으로써, 구현할 수 있습니다. 하지만, 부모 클래스로부터 상속을 받아 자식 클래스에서 새로운 클래스를 만들어서 사용하는 경우, 모든 함수에 virtual 키워드를 붙여야 합니다. 그 이유는 함수의 바인딩에는 정적 바인딩과 동적 바인딩이 있는데, virtual 키워드를 사용하지 않으면 정적 바인딩이 적용되기 때문입니다.

- 가상소멸자

  - virtual 키워드를 소멸자 앞에 붙이는 것을 말합니다. 모든 소멸자에는 virtual 키워드를 넣는 것이 좋습니다.

    ```c++
    Animal* cat = Cat(1, "meow");
    delete cat;
    ```

    위와 같이 cat을 삭제할 때, 정적 바인딩을 했다면, cat을 Animal처럼 취급해서 cat의 소멸자를 호출하지 않고 animal의 소멸자만 호출하게 됩니다.