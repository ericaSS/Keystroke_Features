from scipy.spatial.distance import cityblock
import numpy as np
import pandas

np.set_printoptions(suppress=True)

class KeystrokeManhattanMethod:
    def __init__(self, subjects):
        self.kh_genuine_score = []
        self.kh_impostor_score = []
        self.ki_genuine_score = []
        self.ki_impostor_score = []
        self.kh_frr = 0.0
        self.kh_ipr = 0.0
        self.ki_frr = 0.0
        self.ki_ipr = 0.0
        self.kh_mean_vector = []
        self.ki_mean_vector = []
        self.subjects = subjects

    # calculate the mean(template) of the sample data(200) for
    # keyhold and keyinterval, respectively.
    def calculate_template(self):
        self.kh_mean_vector = self.kh_train.mean().values
        self.ki_mean_vector = self.ki_train.mean().values

    # calculate the manhattan score for key hold and key interval
    def calculate_manhattan_score(self):
        # calculate the key hold manhattan scores
        # key hold genuine score
        for i in range(self.kh_test_genuine.shape[0]):
            current_score = cityblock(self.kh_test_genuine.iloc[i].values, self.kh_mean_vector)
            self.kh_genuine_score.append(current_score)
        # key hold impostor score
        for i in range(self.kh_test_impostor.shape[0]):
            current_score = cityblock(self.kh_test_impostor.iloc[i].values, self.kh_mean_vector)
            self.kh_impostor_score.append(current_score)

        # calculate the key interval manhattan scores
        # key interval genuine score
        for i in range(self.ki_test_genuine.shape[0]):
            current_score = cityblock(self.ki_test_genuine.iloc[i].values, self.ki_mean_vector)
            self.ki_genuine_score.append(current_score)
        # key interval impostor score
        for i in range(self.ki_test_impostor.shape[0]):
            current_score = cityblock(self.ki_test_impostor.iloc[i].values, self.ki_mean_vector)
            self.ki_impostor_score.append(current_score)

    # calculate the false reject and impostor pass rates
    # t for key hold threshold, m for key interval threshold
    def calculate_frr_ipr(self, t, m):
        kh_false_reject = []
        kh_impostor_pass = []
        ki_false_reject = []
        ki_impostor_pass = []

        for i in self.kh_genuine_score:
            if i > t:
                kh_false_reject.append(i)
        self.kh_frr = len(kh_false_reject) / len(self.kh_genuine_score)

        for j in self.kh_impostor_score:
            if j < t:
                kh_impostor_pass.append(j)
        self.kh_ipr = len(kh_impostor_pass) / len(self.kh_impostor_score)

        for i in self.ki_genuine_score:
            if i > m:
                ki_false_reject.append(i)
        self.ki_frr = len(ki_false_reject) / len(self.ki_genuine_score)

        for j in self.ki_impostor_score:
            if j < m:
                ki_impostor_pass.append(j)
        self.ki_ipr = len(ki_impostor_pass) / len(self.ki_impostor_score)

    def run(self):

        for subject in subjects:
            # retrieve the key hold data and set it to genuine and impostor data
            kh_genuine_data = data.loc[data.subject == subject, "H.period":"H.Return"]
            kh_impostor_data = data.loc[data.subject != subject, :]

            # retrieve the key interval data and set it to genuine and impostor data
            ki_genuine_data = data.loc[data.subject == subject, "UD.period.t":"UD.l.Return"]
            ki_impostor_data = data.loc[data.subject != subject, :]

            # fetch the first 200 tests per subject
            self.kh_train = kh_genuine_data[:200]
            # the remaining of 200 tests per subject = 400 - kh_genuine_data
            self.kh_test_genuine = kh_genuine_data[200:]
            # use the first 5 tests to generate the impostor
            self.kh_test_impostor = kh_impostor_data.groupby("subject").head(10).loc[:, "H.period":"H.Return"]

            # same process method for key interval as above
            self.ki_train = ki_genuine_data[:200]
            self.ki_test_genuine = ki_genuine_data[200:]
            self.ki_test_impostor = ki_impostor_data.groupby("subject").head(10).loc[:, "UD.period.t":"UD.l.Return"]

            # run
            self.calculate_template()
            self.calculate_manhattan_score()
            self.calculate_frr_ipr(1.3, 1.5)

            return len(self.kh_genuine_score), len(self.kh_impostor_score), len(self.ki_genuine_score), len(self.ki_impostor_score),\
                self.kh_frr, self.kh_ipr, self.ki_frr, self.ki_ipr


# fetch the data from local
path = ".../Downloads/DSL-StrongPasswordData.csv"
data = pandas.read_csv(path)
subjects = data["subject"].unique()

if __name__ == '__main__':
    print("Keystroke program result: ")
    print("kh_g, kh_i, ki_g, ki_i, kh_frr, kh_ipr, ki_frr, ki_ipr")
    print(KeystrokeManhattanMethod(subjects).run())


