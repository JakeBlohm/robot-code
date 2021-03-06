class Motor:
    CYCLESPERSECOND = 0 # Not needed, but fixes some syntax errors that were annoying
    DEVMODE = True

    motor = []

    def __init__(self, precision, acceleration, maxSpeed, minSpeed):
        self.PRECISION = precision
        self.ACCELERATION = acceleration
        self.MAXSPEED = maxSpeed
        self.MINSPEED = minSpeed

    # Calculate the vector required to move thicc arm
    def MaxVelCalc(self, tarAngle, curAngle, curSpeed):
        if tarAngle > (curAngle - self.PRECISION) and tarAngle < (curAngle + self.PRECISION):
            print("ERROR")
            return 0
        else:
            #fix for the  big if statment below
            if curSpeed == self.MAXSPEED:
                curSpeed -= self.ACCELERATION
            elif curSpeed == -self.MAXSPEED:
                curSpeed += self.ACCELERATION
            #Set target speeds
            difAngle = (tarAngle - curAngle)
            if difAngle >= ((((curSpeed+self.ACCELERATION)/self.ACCELERATION)+1)*(((curSpeed+self.ACCELERATION))/2))/self.CYCLESPERSECOND:
                return self.MAXSPEED
            if difAngle <= -(((((curSpeed-self.ACCELERATION)/self.ACCELERATION)-1)*(((curSpeed-self.ACCELERATION))/2))/self.CYCLESPERSECOND):
                return -self.MAXSPEED
            elif difAngle > 0:
                return self.MINSPEED
            elif difAngle < 0:
                return -self.MINSPEED
            else:
                print("MAJOR ERROR")
    # Set the speed
    def VelCalc(self, tarSpeed, curSpeed):
        difSpeed = (tarSpeed - curSpeed)
        if difSpeed > 0 and curSpeed <= (self.MAXSPEED - self.ACCELERATION):
            curSpeed += self.ACCELERATION
        elif difSpeed < 0 and curSpeed >= (self.ACCELERATION - self.MAXSPEED):
            curSpeed -= self.ACCELERATION
        return curSpeed


    # Encoder will replace
    def EncoderOut(self, curSpeed, motor):
        motor[1] += (curSpeed / self.CYCLESPERSECOND)
        motor[1] = round(motor[1], 4)
        return motor


    def MotorMove(self, motor):
        if motor[0] <= (motor[1] - self.PRECISION) or motor[0] >= (motor[1] + self.PRECISION):
            motor[2] = self.MaxVelCalc(motor[0], motor[1], motor[3])
            motor[3] = self.VelCalc(motor[2], motor[3])
            motor = self.EncoderOut(motor[3], motor)
            if (self.DEVMODE == True):
                print(motor)
        else:
            motor[3] = 0
        return motor

