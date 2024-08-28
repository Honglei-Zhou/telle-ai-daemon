### Telle AI Client Middleware

### Description 
This project is part of Telle AI Chatbot System. The daemon is used to persist data to database

### Interfaces/APIs

```buildoutcfg

message type: dictionary
message: {'type': 'SYS_MSG', 
          'dealerId': dealerId,
          'adminId': adminId,
          'user': 'admin',
          'muted': True,
          'unread': 0,
          'message': message
         }
         
message type: dictionary
message: {'type': 'UPDATE_MSG', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId, # required if user is admin
          'user': 'admin|customer|bot',
          'muted': True|False,
          'unread': 0,
          'message': message
         }
         
message type: dictionary
message: {'type': 'UPDATE_CHAT', 
          'dealerId': dealerId,
          'groupId': groupId, # required if user is customer
          'adminId': admin_id, # required if user is admin
          'user': 'customer|admin',
          'online': True|False
         }
         
message type: dictionary
message: {'type': 'UPDATE_GROUP', 
          'dealerId': dealerId,
          'groupId': groupId,
          'user': 'customer',
          'online': True|False
         }

message type: dictionary
message: {'type': 'UPDATE_USER', 
          'dealerId': dealerId,
          'groupId': groupId,
          'message': message
         }
         
message type: dictionary
message: {'type': 'UPDATE_PAGEVIEW', 
          'dealerId': dealerId,
          'groupId': groupId,
          'message': message
         }
         
message type: dictionary
message: {'type': 'UPDATE_LEAD', 
          'dealerId': dealerId,
          'groupId': groupId,
          'message': message
         }

message type: dictionary
message: {'type': 'CREATE_LEAD_INTENT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'message': message
         }

message type: dictionary
message: {'type': 'UPDATE_LEAD_INTENT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'message': message
         }
```
