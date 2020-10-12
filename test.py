import data_mul
import data_ber
import label
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB


actions = [
    (0, "BanConfig"), (1, "Elite_SA_Create"), (2, "Elite_SA_ReturnPosition"), (3, "Connect7500"), (4, "Connect720x"),
    (5, "Closed7500"), (6, "Closed720x"), (7, "QA_ProductListItemBuyError"), (8, "QA_ProductListItemBuy"),
    (9, "CN_IdLogin"), (10, "QA_ReceiveMoney"), (11, "QA_ReceiveMoneyError"), (12, "QA_CancelDeal"),
    (13, "QA_CancelDealError"), (14, "QA_PurchaseItem"), (15, "QA_PurchaseItemError"), (16, "QA_PurchaseItemExpired"),
    (17, "QA_ItemSalesRegistration"), (18, "QA_ItemSalesRegistrationError"), (19, "QA_ItemSalesRegistrationExpired"),
    (100, "CN_ChannelAwayExpired"), (101, "SN_PreventMacro"), (103, "SN_ShowVioletta"), (104, "QA_ConfirmVioletta"),
    (106, "Party_CQ_Invite"), (107, "Party_QA_Create"), (200, "navigate_no_path"), (201, "CQ_Respawn"),
    (202, "CQ_ReviveReturn"), (203, "CQ_Warp"), (204, "CQ_DirectWarp"), (205, "QA_DirectMove"),
    (206, "QA_StarForceFieldTeleport"), (207, "QA_CheckSkillWarp"), (208, "no_path_DirectWarp"), (1000, "stopped")
]

if __name__ == '__main__':
    train_data_mul = np.array(data_mul.data)
    train_data_ber = np.array(data_ber.data)
    train_label = np.array(label.label)
    one = np.array([[0, 0, 0, 20, 10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]])
    more = np.array([[0, 0, 0, 40, 40, 34, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6]])
    clf = MultinomialNB(alpha=1)
    clf.fit(train_data_mul, train_label)
    print("Multinomial: -------------------------------------")
    print('Predicting class of one:', str(clf.predict(one)[0]))
    print('Probability of one in each class:', clf.predict_proba(one))

    print('Predicting class of more:', str(clf.predict(more)[0]))
    print('Probability of more in each class:', clf.predict_proba(more))

    clf1 = BernoulliNB()
    clf1.fit(train_data_ber, train_label)
    print("Bernoulli  : -------------------------------------")
    print('Predicting class of one:', str(clf1.predict(one)[0]))
    print('Probability of one in each class:', clf1.predict_proba(one))

    print('Predicting class of more:', str(clf1.predict(more)[0]))
    print('Probability of more in each class:', clf1.predict_proba(more))
