from pyod.models.lof import LOF
from pyod.utils import generate_data

from unquad.enums.adjustment import Adjustment
from unquad.estimator.conformal_estimator import ConformalEstimator
from unquad.enums.method import Method
from unquad.estimator.split_configuration import SplitConfiguration
from unquad.evaluation.metrics import false_discovery_rate, statistical_power

if __name__ == "__main__":
    x_train, x_test, y_train, y_test = generate_data(
        n_train=1_000,
        n_test=1_000,
        n_features=10,
        contamination=0.1,
        random_state=1,
    )

    x_train = x_train[y_train == 0]

    sc = SplitConfiguration(n_bootstraps=40, n_calib=1_000)
    ce = ConformalEstimator(
        detector=LOF(),
        method=Method.JACKKNIFE_AFTER_BOOTSTRAP,
        split=sc,
        adjustment=Adjustment.BENJAMINI_HOCHBERG,
        alpha=0.1,
        seed=1,
    )

    ce.fit(x_train)
    estimates = ce.predict(x_test, raw=False)

    print(false_discovery_rate(y=y_test, y_hat=estimates))
    print(statistical_power(y=y_test, y_hat=estimates))