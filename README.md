# RabbitMQ Stream & Record Tool

כלי צד קל להפעלה שמאפשר שידור (stream) והקלטה (record) של הודעות RabbitMQ בצורה נוחה ואינדיקטיבית, דרך קובץ קונפיגורציה פשוט.

## מצבי הרצה

הכלי מופעל בעזרת פרמטר שמציין את מצב ההרצה:

- `stream` – שידור הודעות מתוך תיקייה או S3 ל-Exchange בקצב וזמן מוגדרים.
- `record` – הקלטת הודעות מ-Exchange לקבצים בתיקייה לוקאלית או S3.

## קונפיגורציה לדוגמא:

```yaml
RabbitMq:
  Host: localhost
  Port: 5672
  Username: guest
  Password: guest

Stream:
  Loop: True
  Duration: 60
  Rate: 100
  Exchange: StreamExample
  From: Local
  Local:
    Source: StreamFolderExample
  S3:
    Url: Placeholder
    Bucket: Placeholder
  Redis:
    Url: Placeholder

Record:
  Duration: 60
  Exchange: RecordExample
  To: Local
  Local:
    Destination: RecordFolderExample
  S3:
    Url: Placeholder
    Bucket: Placeholder
  Redis:
    Url: Placeholder
```

## תכונות מרכזיות

- שידור (Stream) של הודעות JSON או קבצים:
  - שליטה בקצב ההודעות (messages per second)
  - הגדרת משך השידור בשניות
  - אפשרות להריץ בלולאה (Loop)
  - תמיכה בקבצים ממקור לוקאלי או S3

- הקלטה (Record) של הודעות:
  - יצירת תור זמני (auto-delete) להאזנה
  - שמירת ההודעות לקבצים בתיקייה לוקאלית או S3
  - שליטה במשך ההאזנה בשניות

- תמיכה ב-S3 כמקור וקובץ יעד

- אפשרות עתידית לשימוש ב-Redis לניהול מצבים (checkpointing וכדומה)

## דוגמאות להרצה

```bash
# שידור הודעות לפי קובץ קונפיגורציה
python main.py stream

# הקלטת הודעות לפי קובץ קונפיגורציה
python main.py record
```

## שימושים אפשריים

- ביצוע בדיקות עומסים (Load Testing)
- סימולציה של מערכות זמן-אמת
- הקלטת תעבורת הודעות לצורך דיבוג או שחזור


## TODO

- - הוספת תמיכה מלאה ב-Redis (קריאה וכתיבה)
- הוספת תמיכה מלאה ב-S3 (קריאה וכתיבה)
- הוספת מנגנוני serialization / deserialization גמישים (למשל JSON, XML, Protobuf)


