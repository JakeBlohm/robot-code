using system;

X = 10;
Y = 10;
Z = 10;


mOneCAngle = ((math.Degrees(math.Acos(ALL_HORIZONTAL_OFFSET/(math.Sqrt((X**2)+(Y**2))))))-(math.Degrees(math.Atan(Y/X))));


tarDistance = (math.Sqrt((Z**2)+((math.Sqrt((X**2)+(Y**2)))**2)));
mTwoCAngle = (90 - ((math.Degrees(math.Atan(Z/X)))+(math.Degrees(math.Acos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))));
mThreeCAngle = (180 - (math.degrees(math.arccos(((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(tarDistance**2))/(2*SEGMENT_TWO*SEGMENT_ONE)))));

print(mOneCAngle, mTwoCAngle, mThreeCAngle);

curDistanceAngled = math.Sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*math.Cos(math.Radians(180-mThreeCAngle))));
AAngle = (90 - (mTwoCAngle+math.Degrees(math.Acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled)))));
curDistance = curDistanceAngled*math.Cos(math.Radians(AAngle));
Y = (curDistance*math.Cos(math.Radians(mOneCAngle)),2);
X = (curDistance*math.Sin(math.Radians(mOneCAngle)),2);
Z = (curDistanceAngled*math.Sin(math.Radians(AAngle)),2);

print(X, Y, Z);