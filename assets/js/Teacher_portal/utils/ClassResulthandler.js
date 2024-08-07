class ClassResulthandler {
  constructor(data) {
    this.students = data;
    this.calculateFields();
  }

  calculateFields() {
    this.students.forEach((student) => {
      student.Total = this.calculateTotal(student);
      student.Ave = this.calculateAverage(student);
      student.Grade = this.calculateGrade(student);
      student.Position = "-";
      student.Remarks = "-";
    });

    // Calculate position based on Total
    this.calculatePosition();

    // Calculate remarks based on Grade
    this.calculateRemarks();
  }

  // this has to be Calulated dynamically
  calculateTotal(student) {
    let total = student.subjects.reduce((sum, subject) => {
      const Total = subject.Total;
      return (
        sum + (isNaN(Total) || Total === "-" ? 0 : parseFloat(Total))
      );
    }, 0);

    return total;
  }

  // this has to be Calulated dynamically
  calculateAverage(student) {
    let validSubjectsCount = student.subjects.reduce((count, subject) => {
      const total = subject.Total;
      return count + (isNaN(total) || total === "-" ? 0 : 1);
    }, 0);

    let Total = this.calculateTotal(student);
    let Average = validSubjectsCount > 0 ? Total / validSubjectsCount : 0;

    return parseFloat(Average.toFixed(2)); 
  }


  calculateGrade(student) {
    if (student.Ave >= 70) return "A";
    else if (student.Ave >= 55) return "C";
    else if (student.Ave >= 40) return "P";
    else return "F";
  }

  calculatePosition() {
    this.students.sort((a, b) => b.Ave - a.Ave);

    // Function to calculate ordinal suffix
    const getOrdinalSuffix = (number) => {
      if (number === 11 || number === 12 || number === 13) {
        return "th";
      } else {
        const lastDigit = number % 10;
        switch (lastDigit) {
          case 1:
            return "st";
          case 2:
            return "nd";
          case 3:
            return "rd";
          default:
            return "th";
        }
      }
    };

    let previousAve = null;
    let previousPosition = null;

    this.students.forEach((student, index) => {
      const currentTotal = student.Ave;
      const suffix = getOrdinalSuffix(index + 1);

      if (currentTotal === previousAve) {
        // Assign the same position as the previous student
        student.Position = previousPosition;
      } else {
        // Assign a new position
        student.Position = `${index + 1}${suffix}`;
      }

      // Update previous total and position
      previousAve = currentTotal;
      previousPosition = student.Position;
    });
  }

  calculateRemarks() {
    this.students.forEach((student) => {
      if (student.Grade === "-") student.Remarks = "-";
      else if (student.Grade === "A") student.Remarks = "Excellent";
      else if (student.Grade === "C") student.Remarks = "Good";
      else if (student.Grade === "P") student.Remarks = "Pass";
      else student.Remarks = "Fail";
    });
  }

  getStudents() {
    return this.students;
  }
}

export default ClassResulthandler;
