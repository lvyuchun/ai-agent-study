from dataclasses import dataclass, field

@dataclass
class Course:
    name: str                # 课程名
    course_id: str           # 课程号
    credits: int             # 学分
    max_students: int = 30   # 容量上限（有默认值，可省略）

@dataclass
class Student:
    name: str
    student_id: str
    courses: dict = field(default_factory=dict)   # ⚠️ 关键写法，见下方讲解

    # === 选课 ===
    def enroll(self, course):
        if course.name in self.courses:
            print(f"⚠️ 已选过 {course.name}")
            return False
        self.courses[course.name] = None   # 成绩先设为 None（还没考试）
        print(f"✅ {self.name} 选了「{course.name}」")
        course.max_students -= 1
        return True

    # === 退课 ===
    def drop(self, course):
        if course.name not in self.courses:
            print(f"❌ 没选过 {course.name}")
            return False
        del self.courses[course.name]
        print(f"🗑️ 退课成功: {course.name}")
        course.max_students += 1
        return True

    # === 打分（老师用）===
    def set_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name] = grade

    # === 查成绩 ===
    def get_grade(self, course_name):
        if course_name not in self.courses:
            print(f"❌ 没选过 {course_name}")
            return None
        g = self.courses[course_name]
        print(f"{course_name} 成绩: {g if g is not None else '未出分'}")
        return g
python = Course("Python 编程", "CS101", 3)
math = Course("高等数学", "MATH101", 4)

s = Student("张三", "20260001")
s.enroll(python)             # ✅ 张三 选了「Python 编程」
s.enroll(python)             # ⚠️ 已选过 Python 编程（防重复）
s.enroll(math)               # ✅ 张三 选了「高等数学」

s.set_grade("Python 编程", 92)
s.get_grade("Python 编程")    # Python 编程 成绩: 92
s.get_grade("高等数学")        # 高等数学 成绩: 未出分

s.drop(python)         # 🗑️ 退课成功
s.get_grade("Python 编程")    # ❌ 没选过 Python 编程

print(s)                      # dataclass 自动生成的 __repr__
# Student(name='张三', student_id='20260001', courses={'高等数学': None})
