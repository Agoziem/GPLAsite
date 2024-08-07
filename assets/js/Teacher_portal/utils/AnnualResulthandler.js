class AnnualResulthandler {
  constructor(data) {
    this.students = data;
    this.calculateFields();
  }

  calculateFields() {
    this.students.forEach((student) => {
      student.Total = this.calculateTotal(student);
      student.Average = this.calculateAverage(student);
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
  // terms = {
  //   "1st Term": 30,
  //   "2nd Term": 30,
  //   "3rd Term": 40,
  // };
  calculateTotal(student) {
    const values = Object.values(student["terms"]);
    const allEmptyOrDash = values.every(
      (value) => value === "-" || value === ""
    );

    if (allEmptyOrDash) {
      return "-";
    }
    return values.reduce(
      (sum, key) => sum + (isNaN(key) ? 0 : parseInt(key)),
      0
    );
  }

  // this has to be Calulated dynamically
  calculateAverage(student) {
    const values = Object.values(student["terms"]);
    const allEmptyOrDash = values.every(
      (value) => value === "-" || value === ""
    );

    if (allEmptyOrDash) {
      return "-";
    }
    const greaterThanOrEqualToOneCount = values.filter(
      (key) => parseInt(key) >= 0 && key !== "-" && key !== ""
    ).length;
    // Check if greaterThanOrEqualToOneCount is not zero before performing the division
    const average =
      greaterThanOrEqualToOneCount !== 0
        ? parseFloat((student.Total / greaterThanOrEqualToOneCount).toFixed(2))
        : 0;

    return average;
  }

  calculateGrade(student) {
    if (student.Average >= 70) return "A";
    else if (student.Average >= 55) return "C";
    else if (student.Average >= 40) return "P";
    else return "F";
  }

  calculatePosition() {
    this.students.sort((a, b) => b.Average - a.Average);

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

    let previousAverage = null;
    let previousPosition = null;

    this.students.forEach((student, index) => {
      const currentTotal = student.Average;
      const suffix = getOrdinalSuffix(index + 1);

      if (currentTotal === previousAverage) {
        // Assign the same position as the previous student
        student.Position = previousPosition;
      } else {
        // Assign a new position
        student.Position = `${index + 1}${suffix}`;
      }

      // Update previous total and position
      previousAverage = currentTotal;
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

export default AnnualResulthandler;
