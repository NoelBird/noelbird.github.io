# week4



c++, jenkins, 최대 부분합 알고리즘을 학습했습니다.



### c++ map
-  키는 중복될 수 없음. C++ 맵은 자동 정렬되는 컨테이너
- map을 정렬하는 방법은 2가지가 있음.
- operator<를 오버라이딩 하는 방법, comparer를 생성하는 방법
- 클래스를 바꿀 권한이 있으면, 전자의 방법이 더 좋음



### jenkins
  - jenkins에서 github 연동 가능
  - pull request 행위만 따로 감지할 수도 있음.
  - 이 부분은 github에서 web hook의 종류를 바꾸면 가능함



### 템플릿 프로그래밍
- 템플릿 구현체를 header에 넣어야 함.
- 이렇게 하지 않고 cpp 파일에 넣으면, template의 구현체를 찾을 수 없어서 오류가 발생함
- 템플릿 특수화(전체 템플릿 특수화)
  ```c++
    template<typename VAL, typename EXP>
    VAL Power(const VAL value, EXP exponent) {} // 모든 형을 받는 제네릭 power()

    template <>
    float Power(float value, float exp) // float을 받도록 특수화된 power()
  ```
- 템플릿 특수화(부분 템플릿 특수화)
  ```c++
    template <class T, class Allocator>
    class std::vector<T, allocator> {} // 모든 형을 받는 제네릭 vector

    template<class Allocator>
    class std::vector<bool, Allocator> // bool을 받도록 특수화된 vector
  ```



### c++11

- 11에서 추가된 키워드 목록: auto, static_assert, default/delete, final/override
- auto보다는 auto& 사용(명확함)
- auto& 보다는 const auto& 사용



### 최대 부분합 알고리즘
```c++
// O(n)의 알고리즘. arr[i]값과 sum + arr[i] 값을 비교해서 값이 큰 sequence를 유지
int solve3(int* arr, size_t n)
{
	int max = 0;
	int sum = 0;

	for (int i = 0; i < n; ++i)
	{
		sum = arr[i] > sum + arr[i] ? arr[i] : sum + arr[i];
		max = sum > max ? sum : max;
	}
	return max;
}
```

